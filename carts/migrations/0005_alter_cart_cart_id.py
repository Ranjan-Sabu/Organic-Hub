# Generated by Django 4.2.7 on 2023-12-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.IntegerField(blank=True, max_length=255),
        ),
    ]