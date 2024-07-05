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
    RecipeListView,
    create_recipe,
    RecipeDetailView,
    DietCreateView,
    DietDeleteView,
    DietUpdateView,
    DietListView
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
    path("create_diet/", DietCreateView.as_view(), name="create_diet"),
    path("delete_diet/<int:pk>", DietDeleteView.as_view(), name="delete_diet"),
    path("update_diet/<int:pk>", DietUpdateView.as_view(), name="update_diet"),
    path("diet_list/", DietListView.as_view(), name="diet_list"),
    path("create_recipe/", create_recipe, name="create_recipe"),
    path("recipes/", RecipeListView.as_view(), name= 'recipe_list'),
    path("recipes/<int:pk>", RecipeDetailView.as_view(), name='recipe')
]

app_name = "recipe"
