from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='home'),

    # Дії із користувачем
    path('register/', RegisterUser.as_view(), name="register_user"),
    path('login/', auth_views.LoginView.as_view(template_name='mainapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mainapp/logout.html'), name='logout'),
    path('profile/', login_required(ProfilePage.as_view()), name="profile"),

    # Дії із моделю Client
    path('clients/', ClientListView.as_view(), name="client_list"),
    path('client_update/<int:pk>/', login_required(ClientUpdate.as_view()), name="client_update"),

    # Дії із моделю Stock
    path('stocks/', StockListView.as_view(), name='stock_list'),
    path('stocks/<int:pk>/', StockDetailView.as_view(), name="stock_detail"),

    # Дії із моделю Portfolio
    path('portfolio/<int:pk>/', login_required(PortfolioDetailView.as_view()), name="portfolio_detail"),
    path('portfolio_add/', login_required(PortfolioCreateView.as_view()), name="portfolio_create"),

    #Дії із моделю Transaction
    path("transaction_create/", login_required(TransactionCreateView.as_view()), name="transaction_create"),

    # Додаткові дії
    path('upload_csv/', staff_member_required(CsvUploadFormView.as_view()), name="upload_csv"),
    path('stock-autocomplete/', login_required(StockAutocomplete.as_view()), name="stock-autocomplete"),
]