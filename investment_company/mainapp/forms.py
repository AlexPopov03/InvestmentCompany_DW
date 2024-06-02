from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Client, Portfolio, Transaction, Stock
from dal import autocomplete, forward

class UserRegisterForm(UserCreationForm):
    email = forms.CharField(
        required=True, 
        widget=forms.EmailInput(
            attrs={
                'class': 'validate',
                }
            )
        )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClientUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50, 
        label="Ім'я", 
        help_text="Ваше повне ім'я"
        )
    surname = forms.CharField(
        max_length=50, 
        label='Прізвище',
        help_text="Ваше прізвище"
        )
    email = forms.CharField(
        required=True, 
        widget=forms.EmailInput(
            attrs={
                'class': 'validate',
                }
            )
        )
    phone_number = PhoneNumberField(
        label='Номер телефону')
    class Meta:
        model = Client
        fields = ['name', 'surname', 'email', 'phone_number']

class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['portfolio_name',]

class TransactionCreateForm(forms.ModelForm):
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.none())
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='stock-autocomplete',
            forward=(forward.Field('portfolio'),
                     forward.Field('transaction_type'),),
        )
    )
    transaction_type = forms.ChoiceField(choices=Transaction.TRANSACTION_TYPE)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        portfolio_qs = Portfolio.objects.filter(client=user.client)
        self.fields['portfolio'].queryset = portfolio_qs

    class Meta:
        model = Transaction
        fields = ['portfolio', 'stock', 'stock_ammount', 'transaction_type']

class UploadFileForm(forms.Form):
    file_name = forms.CharField(max_length=100, required=False)
    file = forms.FileField()