from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "firstname",
            "lastname",
            "phone",
            "email",
            "address",
            "country",
            "state",
            "city",
            "order_note",
        ]
