# Generated by Django 5.0.6 on 2024-07-16 10:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_system", "0004_remove_customuser_email_is_verified_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userpreference",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="preference",
                to=settings.AUTH_USER_MODEL,
                unique=True,
            ),
        ),
    ]
