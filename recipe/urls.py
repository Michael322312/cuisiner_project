from django.urls import path
from recipe.views import (
    CategoryListView,
    CategoryDeleteView,
    CategoryCreateView,
    CategoryUpdateView,
    ProductListView,
    ProductDeleteView,
    ProductUpdateView,
    ProductCreateView,
    RecipeCreateView,
    manage_recipes,
)
from django.urls import reverse_lazy

urlpatterns = [
    path("category_list/", CategoryListView.as_view(), name="category_list"),
    path("delete_category/<int:pk>", CategoryDeleteView.as_view(), name="delete_category"),
    path("create_category/", CategoryCreateView.as_view(), name="create_category"),
    path("update_category/<int:pk>", CategoryUpdateView.as_view(), name="update_category"),
    path("product_list/", ProductListView.as_view(), name="product_list"),
    path("create_product/", ProductCreateView.as_view(), name="create_product"),
    path("delete_product/<int:pk>", ProductDeleteView.as_view(), name="delete_product"),
    path("update_product/<int:pk>", ProductUpdateView.as_view(), name="update_product"),
    path("create_recipe/<int:id>", manage_recipes, name="create_recipe"),
    path("create_recipe/", manage_recipes, name="create_recipe"),
]

app_name = "recipe"
