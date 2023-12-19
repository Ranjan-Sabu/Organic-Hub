from django.db import models
from store.models import Product
from Accounts.models import Registration

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Registration,models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.FloatField()
    is_active = models.BooleanField(default=True)
    in_guest_cart = models.BooleanField(default=False)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"CartItem {self.id} - {self.product}"