from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class Client(models.Model):
    ''' Модель яка відповідає за уявлення клієнта в базі даних.\n
        Дана модель пов'язана із такими моделями:\n
            1) User (Один до Одного)\n
        Має наступних дітей:\n
            1) Portfolio (Один до Багатьох)\n
        Має наступні поля:\n
            1) name\n
            2) surname\n
            3) email\n
            4) phone_number\n
            5) account\n'''
    name = models.CharField(
        blank=False,
        help_text="Ім'я клієнта",
        max_length=50,
        )
    surname= models.CharField(
        blank=False,
        null=True,
        help_text="Прізвище клієнта",
        max_length=50,
        )
    email=models.EmailField(
        blank=False,
        unique=True,
        help_text="Електронна пошта клієнта",
        )
    phone_number= PhoneNumberField(
        blank=False,
        unique=True,
        null=True,
        help_text="Телефонний номер клієнта",
        )
    account=models.OneToOneField(
        User,
        blank=True,
        on_delete=models.CASCADE,
        )
    first_login = models.BooleanField(
        blank=False,
        default=True,
        help_text="Чи закінчив користувач реєстрацію(ввів детальну інформацію про себе)"
    )

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def Meta(self):
        ordering = ["-name"]

class Stock(models.Model):
    ''' Модель яка відповідає за уявлення Акції в базі даних.\n
        Дана модель має наступних дітей:\n
            1) Transaction (Один до Багатьох)\n
            2) StockPrice (Один до Одного)\n
        Має наступні поля:\n
            1) symbol\n
            2) company_name\n
            3) current_price\n
            4) volume\n
            5) net_change\n
            6) percent_change\n
            7) market_capitalization\n
            8) country\n
            9) ipo\n
            10) sector\n
            11) industry\n
            12) last_price_change (неможливо редагувати)\n
            '''
    symbol= models.CharField(
        blank=False,
        unique=True,
        help_text="Короткий символ акції корпорації (напр.: TSLA для Tesla)",
        max_length=10,
        )
    company_name= models.CharField(
        blank=False,
        help_text="Повна назва компанії",
        max_length=500,
        )
    current_price= models.DecimalField(
        blank=False,
        help_text="Поточна ціна акції", 
        max_digits=16, 
        decimal_places=2,
        )
    volume= models.IntegerField(
        blank=False,
        help_text="Загальна кількість акцій, які були обмінені для даної акції за день",
        )
    net_change= models.DecimalField(
        blank=True,
        null=True,
        help_text="Різниця між поточною ціною та ціною закриття попереднього дня", 
        max_digits=16, 
        decimal_places=2,
        )
    percent_change= models.DecimalField(
        blank=True,
        null=True,
        help_text="Відсоткова зміна ціни акцій або цінного паперу в порівнянні із ціною закриття попереднього дня", 
        max_digits=5, 
        decimal_places=2,
        )
    market_capitalization= models.DecimalField(
        blank=False,
        help_text="Загальна ринкова вартість всіх випущених акцій компанії", 
        max_digits=23, 
        decimal_places=2,
        )
    country= models.CharField(
        blank=False,
        help_text="Країна, в якій знаходиться або має своє головне підрозділ компанія",
        max_length=100,
        )
    ipo= models.PositiveIntegerField(
        blank=False,
        null = True,
        validators=[
            MinValueValidator(1800), 
            MaxValueValidator(datetime.datetime.now().year)],
        help_text="Рік, коли компанія вийшла на публічний ринок, випустивши свою першу публічну пропозицію акцій. Формат: YYYY.",
        )
    sector= models.CharField(
        blank=False,
        help_text="Широка категорія, яка класифікує компанії в різні групи на основі характеру їхньої діяльності", 
        max_length=100,
        )
    industry= models.CharField(
        blank=False,
        help_text="Більш конкретна класифікація, яка подальш розділяє компанії в межах сектора відповідно до їхнього конкретного напрямку діяльності чи пропозицій продуктів/послуг", 
        max_length=100,
        )
    last_price_change= models.DateTimeField(
        blank=True,
        help_text="Останній раз, коли була перевіренна ціна на одну акцію", 
        auto_now=True,
        auto_now_add=False,
        )
    
    def __str__(self):
        return self.symbol
    
    def Meta(self):
        ordering = ["-symbol"]

class StockPrice(models.Model):
    ''' Модель яка відповідає за збереження змін цін на акцію.\n
        Дана модель пов'язана із такими моделями:\n
            1) Stock (Багато до Одного)\n
        Має наступні поля:\n
            1) stock\n
            2) price\n
            3) save_date'''
    stock = models.ForeignKey(
        Stock,
        help_text="Для якої акції зберігаються ціни",
        on_delete=models.CASCADE,
        )
    price = models.DecimalField(
        blank=False,
        help_text="Ціна акції", 
        max_digits=16, 
        decimal_places=2,
        )
    save_date = models.DateTimeField(
        blank=False,
        help_text="Дата, коли данна ціна була в акції",
        auto_now = False,
        auto_now_add=False,
    )
    
    def __str__(self):
        return f"Ціни {self.stock.symbol}"
    
    def Meta(self):
        ordering = ["-stock"]

class Portfolio(models.Model):
    ''' Модель, яка відповідає за уявлення інвестиційного портфелю клієнта.\n
        Дана модель пов'язана із наступними моделями:\n
            1) Client (Багато до Одного)\n
        Дана модель має наступних дітей:\n
            1) Transaction (Один до Багатьох)\n
        Має наступні поля:\n
            1) client\n
            2) portfolio_name\n
            3) creation_date (неможливо редагувати)\n'''
    client = models.ForeignKey(
        Client, 
        help_text="Якому клієнту належить даний інвестиційний портфель", 
        on_delete=models.CASCADE,
        )
    portfolio_name = models.CharField(
        blank=False,
        help_text="Назва інвестиційного портфелю", 
        max_length=100,
        )
    creation_date = models.DateTimeField(
        blank=True,
        help_text="Дата та час, коли був створений портфель. Додається автоматично", 
        auto_now=False, 
        auto_now_add=True,
        )
    
    def __str__(self):
        return f"Портфель {self.portfolio_name}"
    
    def investment(self):
        total_investment = 0
        for transaction in self.transaction_set.all():
            if transaction.transaction_type == 'BUY':
                total_investment += transaction.price
        return round(total_investment, 2)
    
    def value(self):
        total_value = 0
        for transaction in self.transaction_set.all():
            # if transaction.transaction_type == 'BUY':
            #     total_value += transaction.current_transaction_value()
            # elif
            match transaction.transaction_type:
                case 'BUY':
                    total_value += transaction.current_transaction_value()
                case 'SELL':
                    total_value -= transaction.current_transaction_value()
        return round(total_value, 2)

    def profit(self):
        return round(self.value() - self.investment(), 2)
    
    def get_all_buy_stock_symbols(self):
        symbol_list = []
        for transaction in self.transaction_set.all():
            if transaction.transaction_type == 'BUY' and not transaction.stock.symbol in symbol_list:
                    symbol_list.append(transaction.stock.symbol)
        return symbol_list

    def get_all_buy_stock_prices(self):
        prices_dict = {}
        already_added_symbols = []
        for transaction in self.transaction_set.all():
            if transaction.transaction_type == 'BUY': 
                if not transaction.stock.symbol in already_added_symbols:
                    prices_dict[transaction.stock.symbol] = transaction.current_transaction_value()
                    already_added_symbols.append(transaction.stock.symbol)
                else:
                    prices_dict[transaction.stock.symbol] += transaction.current_transaction_value()
        return prices_dict

    def get_all_related_buy_stocks(self):
        related_stocks = []
        for transaction in self.transaction_set.all():
            if not transaction.stock in related_stocks:
                related_stocks.append(transaction.stock)
        return related_stocks

    def get_all_related_stocks_ammount(self):
        related_stocks_ammount = {}
        for transaction in self.transaction_set.all():
            if not transaction.stock.symbol in related_stocks_ammount:
                related_stocks_ammount[transaction.stock.symbol] = transaction.stock_ammount
            else:
                related_stocks_ammount[transaction.stock.symbol] += transaction.stock_ammount
        return related_stocks_ammount
    
    def Meta(self):
        ordering = ["-portfolio_name"]

class Transaction(models.Model):
    ''' Модель яка відповідає за уявлення транзакцій по додаванню чи видаленню
        акцій з інвестиційного портфелю.\n
        Дана модель пов'язана із наступними моделями:\n
            1) Portfolio (Багато до одного)\n
            2) Stock (Багато до одного)\n
        Має наступні поля:\n
            1) portfolio\n
            2) stock\n
            3) stock_ammount\n
            4) price\n
            5) transaction_type\n
            6) deal_date (неможливо редагувати)\n'''
    portfolio = models.ForeignKey(
        Portfolio, 
        help_text="Портфель, з яким проводиться транзакція",
        on_delete=models.CASCADE,
        )
    stock = models.ForeignKey(
        Stock, 
        help_text="З якою акцією проводиться транзакція",
        on_delete=models.CASCADE,
        )
    stock_ammount = models.IntegerField(
        blank=False,
        help_text="Кількість акцій, з якими проводиться транзакція",
        )
    price = models.DecimalField(
        blank=False,
        help_text="Вартість транзакції", 
        max_digits=23, 
        decimal_places=7,
        )
    #  Створення вибору для поля transaction_type
    BUY = "BUY"
    SELL = "SELL"
    TRANSACTION_TYPE = {
        BUY: "Купівля",
        SELL: "Продаж"
    }
    transaction_type = models.CharField(
        blank=False,
        help_text="Тип транзакції", 
        max_length=4,
        choices=TRANSACTION_TYPE,
        default=BUY,
        )
    deal_date = models.DateTimeField(
        blank=False,
        help_text="Дата та час ухвалення транзакції", 
        auto_now_add=True,
        )

    def __str__(self):
        action = ''
        word_change = ''
        match self.transaction_type:
            case self.BUY:
                action = self.TRANSACTION_TYPE[self.BUY]
                word_change = 'у портфель'
            case self.SELL:
                action = self.TRANSACTION_TYPE[self.SELL]
                word_change = 'з портфелю'
        return f"{action} акції {self.stock.symbol} {word_change} {self.portfolio.portfolio_name}"
    
    def current_transaction_value(self):
        return self.stock_ammount * self.stock.current_price
    
    def Meta(self):
        ordering = ["-deal_date"]