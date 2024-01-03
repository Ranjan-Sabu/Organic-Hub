from django import forms
from category.models import Category
from store.models import Product
from order.models import Order


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "status",