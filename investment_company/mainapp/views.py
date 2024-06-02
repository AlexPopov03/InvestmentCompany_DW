from django.views.generic import TemplateView, ListView, FormView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from dal import autocomplete
from .models import *
from .forms import *
from investment_company.settings import BASE_DIR
import csv
import os
import traceback

# Класс для зміни кольору повідомлень в консолі
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# -----------Вигляди, пов'язані із моделями Client, User-----------
class ClientListView(ListView):
    model = Client
    context_object_name = 'clients'
    title = 'Список клієнтів'
    extra_context = {
        "title": title,
    }

class ClientUpdate(UpdateView):
    template_name = 'mainapp/client_update.html'
    model = Client
    fields = ['name', 'surname', 'email', 'phone_number']
    success_url = '/home/profile/'

    def form_valid(self, form):
        if not self.request.user.client.first_login:
            form.save()
        else:
            self.object = form.save(commit=False)
            self.object.first_login = False
            self.object.save()
        return super().form_valid(form)

class RegisterUser(FormView):
    template_name = 'mainapp/register.html'
    form_class = UserRegisterForm
    success_url = '/home/login/'
    title = "Створення нового користувача"
    extra_context = {
        "title": title
    }
    
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Успішно створено аккаунт {username}!')
        return super().form_valid(form)

class ProfilePage(TemplateView):
    template_name = 'mainapp/profile.html'
# ---------------------------------------------------------------  
    
# ------------Вигляди, пов'язані із моделю Stock----------------
class StockListView(ListView):
    model = Stock
    context_object_name = 'stocks'
    title = 'Cписок акцій'
    paginate_by = 100
    extra_context = {
        "title": title,
    }

class StockDetailView(DetailView):
    model = Stock
    context_object_name = 'stock'

class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Stock.objects.none()
        
        portfolio = self.forwarded.get('portfolio', None).replace('Портфель ', '')
        transaction_type = self.forwarded.get('transaction_type', None)
        print(f'portfolio: {portfolio}, transaction_type: {transaction_type}')
        qs = Stock.objects.all()
        if portfolio:
            if transaction_type == 'SELL':
                qs = qs.filter(transaction__transaction_type='BUY', transaction__portfolio=portfolio).order_by('symbol').distinct('symbol')
        if self.q:
            qs = qs.filter(symbol__istartswith=self.q)
        return qs
# ---------------------------------------------------------------  

# Вигляди, пов'язані із моделю Portfolio
class PortfolioDetailView(UserPassesTestMixin, DetailView):
    model = Portfolio
    context_object_name = 'portfolio'

    def test_func(self):
        return self.get_object() in self.request.user.client.portfolio_set.all()

class PortfolioCreateView(FormView):
    form_class = PortfolioCreateForm
    success_url = '/home/profile/'
    template_name = 'mainapp/portfolio_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = self.request.user.client
        self.object.save()
        return super().form_valid(form)
# ---------------------------------------------------------------  
    
# ---------Вигляди, пов'язані із моделю Transaction-------------
class TransactionCreateView(FormView):
    template_name= 'mainapp/transaction_create.html'
    form_class = TransactionCreateForm
    success_url = '/home/profile/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.price = self.object.current_transaction_value()
        self.object.save()
        return super().form_valid(form)
    

    def get_form_kwargs(self):
        kwargs = super(TransactionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
# --------------------------------------------------------------- 
    
# -----------------------Інші вигляди---------------------------
class CsvUploadFormView(FormView):
    template_name = 'mainapp/upload.html'
    form_class = UploadFileForm
    success_url = '/home/'

    def form_valid(self, form):
        self.handle_csv_file()
        return super().form_valid(form)
    
    def handle_csv_file(self):
        file_name = ''
        if self.request.POST['file_name'] == '':
            file_name = self.request.FILES['file'].name.replace('.csv', '')
        else:
            file_name = self.request.POST['file_name']
        file_to_handle = f"{BASE_DIR}/mainapp/uploads/{file_name}.csv"
    
        with open(file_to_handle, 'wb+') as destination:
            for chunk in self.request.FILES['file'].chunks():
                destination.write(chunk)
        
        with open(file_to_handle) as csv_source:
            csvreader = csv.reader(csv_source)
            header = next(csvreader)
            for row in csvreader:
                if not Stock.objects.filter(symbol=row[0]).exists():
                    if not row[5]=='':
                        try:
                            new_stock = Stock(
                                symbol = row[0],
                                company_name = row[1],
                                current_price = float(row[2].replace('$', '')),
                                volume = int(row[8]),
                                net_change = float(row[3]),
                                percent_change = float(row[4].replace('%', '')),
                                market_capitalization = int(row[5].replace('.00', '')),
                                country = row[6],
                                ipo = None if row[7]=='' else row[7],
                                sector = row[9],
                                industry = row[10]
                            )
                            new_stock.save() # INSERT
                        except Exception as e:
                            print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC} Adding stock {row[0]} to DB has produced next error:\n{traceback.format_exc()}")
                else:
                    curr_stock = Stock.objects.get(symbol=row[0])
                    try:
                        curr_stock.current_price = float(row[2].replace('$', ''))
                        curr_stock.net_change = float(row[3])
                        curr_stock.percent_change = float(row[4].replace('%', ''))
                        curr_stock.market_capitalization = int(row[5].replace('.00', ''))
                        curr_stock.volume = int(row[8])
                        curr_stock.save() # UPDATE
                    except Exception as e:
                        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Updating stock {curr_stock.symbol} in DB has produced next error:\n{traceback.format_exc()}") 
        
        if os.path.exists(file_to_handle):
            os.remove(file_to_handle)
        else:
            print("The file does not exist.")

class IndexPage(TemplateView):
    template_name = 'mainapp/index.html'
    title = "Investment Company"
    extra_context = {
        "title": title,
    }

# ---------------------------------------------------------------  