# Generated by Django 4.2.6 on 2023-12-21 12:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0010_remove_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="in_guest_cart",
        ),
    ]
