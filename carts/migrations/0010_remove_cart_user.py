# Generated by Django 4.2.7 on 2023-12-16 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0009_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="user",
        ),
    ]
