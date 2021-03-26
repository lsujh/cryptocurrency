from django import forms

from .list_currency import list_currency
from .models import Invoice


class CurencyForm(forms.Form):
    currency = forms.ChoiceField(choices=list_currency, label="Валюта")


class CreateInvoiceForm(forms.ModelForm):
    number_invoice = forms.CharField(
        label="Номер счета", widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    name_coin = forms.CharField(
        label="Монета", widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    vs_currency = forms.CharField(
        label="Валюта", widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    current_price = forms.FloatField(
        label="Цена", widget=forms.NumberInput(attrs={"readonly": "readonly"})
    )
    amount = forms.IntegerField(label="Количество", initial=1)

    class Meta:
        model = Invoice
        fields = (
            "number_invoice",
            "name_coin",
            "vs_currency",
            "current_price",
            "amount",
        )
