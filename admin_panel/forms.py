from django import forms
from category.models import Category
from store.models import Product


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
