# Generated by Django 4.2.6 on 2023-12-21 12:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_product_quantity_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="quantity_unit",
            field=models.CharField(
                choices=[("Kilogram", "Kg"), ("Liter", "L"), ("piece", "Piece")],
                default="Kg",
                max_length=20,
            ),
        ),
    ]
