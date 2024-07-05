from django.db import models
from django.contrib.auth.models import AbstractUser
from recipe.models import Product, Category, Diet
import core.settings

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="user_system", blank=True, null=True)
    intro = models.TextField(blank=True, null=True)


class UserPreference(models.Model):
    user = models.ForeignKey(core.settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    fav_categories = models.ManyToManyField(Category, blank=True, related_name="fav_categories")
    hate_categories = models.ManyToManyField(Category, blank=True, related_name="hate_categories")

    fav_products = models.ManyToManyField(Product, blank=True, related_name="fav_products")
    hates_products = models.ManyToManyField(Product, blank=True, related_name="hate_products")

    diet = models.ManyToManyField(Diet, blank=True)
