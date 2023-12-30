# Generated by Django 4.2.7 on 2023-11-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Registration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=100)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superadmin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
