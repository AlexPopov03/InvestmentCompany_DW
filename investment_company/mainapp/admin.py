from django.contrib import admin
from .models import Client, Stock, StockPrice, Portfolio, Transaction

# Register your models here.
class PortfolioInline(admin.StackedInline):
    model = Portfolio
    extra = 5

class TransactionInline(admin.StackedInline):
    model = Transaction

class StockPriceInline(admin.StackedInline):
    model = StockPrice
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [PortfolioInline]
    list_display = ['name', 'surname', 'account', 'email', 'phone_number']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    inlines=[StockPriceInline, TransactionInline]
    list_display = ["symbol", "company_name", "sector", "industry", "last_price_change"]

@admin.register(StockPrice)
class StockPrice(admin.ModelAdmin):
    list_display = ["stock"]

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]
    list_display = ["portfolio_name", "client", "creation_date"]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "portfolio"]
