# Generated by Django 5.0.6 on 2024-08-01 10:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0012_recipe_likes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingridient",
            options={"ordering": ["id"]},
        ),
    ]
