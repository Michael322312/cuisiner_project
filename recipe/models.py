from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import core.settings
import re


def embed_url(video_url):
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]+)"
    return re.sub(regex, r"https://www.youtube.com/embed/\1",video_url)

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


class Diet(models.Model):
    name = models.CharField(max_length=23)
    forriben_categories = models.ManyToManyField(Category)
    caloires_per_dish = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class RecipeIngridient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="recipe_ingridients")
    weight = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    weight_unit = models.CharField(max_length=23, choices=UNIT_CHOISES, default="G")
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )

    def __str__(self):
        return f"{self.product} {self.weight} {self.weight_unit}"
    
    class Meta:
        ordering = ["-id"]


class Recipe(models.Model):
    author = models.ForeignKey(core.settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=63)
    main_image = models.ImageField(upload_to="recipe/", blank=True)
    url_yt_video = models.URLField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    recipe_text = models.TextField()
    upload_date = models.DateField(auto_now=True)
    total_calories = models.IntegerField(default=0)
    is_dividible = models.BooleanField(default=False)

    def calculate_total_calories(self):
        unit_type = {
            "small": ["ML", "G"],
            "big": ["L", "KG"],
            "un_div": ["Pieces"]
        }
        total_calories = 0

        for ingredient in self.ingredients.all():
            result = ingredient.product.calories * ingredient.weight

            if ingredient.weight_unit in unit_type["small"]:
                total_calories += result / 100 
            elif ingredient.weight_unit in unit_type["big"]:
                total_calories += result * 10
            elif ingredient.weight_unit in unit_type["un_div"]:
                total_calories += result / 100 * ingredient.piece_weight

        return total_calories
    
    def save(self, *args, **kwargs):
        if self.url_yt_video:
            self.url_yt_video = embed_url(self.url_yt_video)
        super(Recipe, self).save(*args, **kwargs)

        total_calories = self.calculate_total_calories()
        self.total_calories = total_calories

        super(Recipe, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-id']


@receiver(pre_delete, sender=Recipe)
def image_model_delete(sender, instance, **kwargs):
    if instance.main_image.name:
        instance.main_image.delete(False)