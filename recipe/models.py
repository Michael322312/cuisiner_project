from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

UNIT_CHOISES = [("ML", "ml"), ("L", "l"), ("G", "g"), ("KG", "kg"), ("PIECES","pcs")]

class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-id"]


class Product(models.Model):
    name = models.CharField(max_length=63, unique=True)
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

    piece_weight = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)], blank=True,  null=True
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
    main_image = models.ImageField(upload_to="recipe/", blank=True)
    url_yt_video = models.URLField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    recipe_text = models.TextField()
    upload_date = models.DateField(auto_now=True)
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
            elif recipe_ingredient.weight_unit == "PEICES":
                total_calories += (
                    recipe_ingredient.product.calories / 100 * recipe_ingredient.weight * recipe_ingredient.piece_weight
                )

        return total_calories
    
    class Meta:
        ordering = ['-id']


@receiver(pre_delete, sender=Recipe)
def image_model_delete(sender, instance, **kwargs):
    if instance.main_image.name:
        instance.main_image.delete(False)