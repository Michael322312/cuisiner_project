# Generated by Django 5.0.6 on 2024-07-05 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0008_diet_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diet",
            name="name",
            field=models.CharField(max_length=23),
        ),
    ]
