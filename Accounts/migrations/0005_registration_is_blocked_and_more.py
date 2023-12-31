# Generated by Django 4.2.6 on 2024-01-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Accounts", "0004_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="registration",
            name="is_blocked",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(max_length=10),
        ),
    ]
