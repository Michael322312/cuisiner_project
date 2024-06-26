from django.contrib import admin
from recipe.models import Category, Product, RecipeIngridient, Recipe

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(RecipeIngridient)
admin.site.register(Recipe)
