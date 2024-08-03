from django.db import models
from django.contrib.auth.models import AbstractUser
from recipe.models import Product, Category, Diet, Recipe
from django.db.models import Q
import core.settings


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="user_system", blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    favorite = models.ManyToManyField(
        Recipe,
        related_name="users_favorite",
        blank=True
    )


class UserPreference(models.Model):
    user = models.OneToOneField(
        core.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preference",
        unique=True
    )

    fav_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="fav_categories"
    )
    hate_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="hate_categories"
    )

    fav_products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="fav_products"
    )
    hates_products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="hate_products"
    )

    diet = models.ManyToManyField(Diet, blank=True)


    def recipe_prefernce_filter(self, for_user):
        if for_user:
            recipes_for_user = Recipe.objects

            if for_user in ["hated", "all"]:
                recipes_for_user = recipes_for_user.exclude(
                    Q(ingredients__product__category__in=self.hate_categories.all())|
                    Q(ingredients__product__in=self.hates_products.all())
                )
            if for_user in ["favorite", "all"]:
                recipes_for_user = recipes_for_user.filter(
                    Q(ingredients__product__category__in=self.fav_categories.all()) |
                    Q(ingredients__product__in=self.fav_products.all())
                )
            return recipes_for_user
        return None
