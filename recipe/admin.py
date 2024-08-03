from django.contrib import admin
from recipe.models import Category, Product, RecipeIngridient, Recipe, Diet


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(RecipeIngridient)
admin.site.register(Recipe)
admin.site.register(Diet)
