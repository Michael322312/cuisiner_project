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
