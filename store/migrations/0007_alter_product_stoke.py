# Generated by Django 4.2.6 on 2024-01-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_alter_product_quantity_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="stoke",
            field=models.FloatField(default=0),
        ),
    ]
