from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.

QUANTITY_UNIT_CHOICES = [
    ("Kg", "Kg"),
    ("L", "L"),
    ("piece", "Piece"),
    # Add more choices as needed
]


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="photos/products")
    stoke = models.FloatField(default=0)
    quantity_unit = models.CharField(
        max_length=20, choices=QUANTITY_UNIT_CHOICES, default="Kg"
    )
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.stoke < 0:
            self.stoke = 0

        super(Product, self).save(*args, **kwargs)
        
    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
