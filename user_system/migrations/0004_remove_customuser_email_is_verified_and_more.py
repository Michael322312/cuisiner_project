# Generated by Django 5.0.6 on 2024-07-15 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_system", "0003_customuser_email_is_verified_alter_customuser_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="email_is_verified",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
    ]
