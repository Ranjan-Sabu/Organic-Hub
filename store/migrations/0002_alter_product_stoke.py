# Generated by Django 4.2.7 on 2023-12-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="stoke",
            field=models.FloatField(),
        ),
    ]
