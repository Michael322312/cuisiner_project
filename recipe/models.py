from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


UNIT_CHOISES = [("ML", "ml"), ("L", "l"), ("G", "g"), ("KG", "kg")]

class Category(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-id"]


class Product(models.Model):
    name = models.CharField(max_length=63)
    calories = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class RecipeIngridient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    weight = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    weight_unit = models.CharField(max_length=23, choices=UNIT_CHOISES, default="G")
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )

    def __str__(self):
        return f"{self.product} {self.weight} {self.weight_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=63)
    main_image = models.ImageField(upload_to="recepie/", blank=True, null=True)
    url_yt_video = models.URLField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    recipe_text = models.TextField()
    total_calories = models.IntegerField(default=0)

    def calculate_total_calories(self):
        total_calories = 0
        for recipe_ingredient in self.ingredients.all():
            if (
                recipe_ingredient.weight_unit == "ML"
                or recipe_ingredient.weight_unit == "G"
            ):
                total_calories += (
                    recipe_ingredient.product.calories / 100 * recipe_ingredient.weight
                )
            elif (
                recipe_ingredient.weight_unit == "L"
                or recipe_ingredient.weight_unit == "KG"
            ):
                total_calories += (
                    recipe_ingredient.product.calories * 10 * recipe_ingredient.weight
                )

        return total_calories

