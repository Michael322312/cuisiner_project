from django.db import models
from django.contrib.auth.models import AbstractUser
from recipe.models import Product, Category, Diet

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="user_system", blank=True, null=True)
    intro = models.TextField(blank=True, null=True)


class UserPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

    likes_categories = models.ManyToManyField(Category, blank=True, null=True)
    hates_categories = models.ManyToManyField(Category, blank=True, null=True)

    likes_products = models.ManyToManyField(Product, blank=True, null=True)
    hates_products = models.ManyToManyField(Product, blank=True, null=True)

    diet = models.ManyToManyField(Diet, blank=True, null=True)
