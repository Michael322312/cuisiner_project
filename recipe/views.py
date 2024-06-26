from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.core.paginator import Paginator
from django.template.defaulttags import register
from recipe.models import Category, Product, RecipeIngridient, Recipe
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from recipe.forms import CategoryCreateForm, ProductCreateForm, RecipeCreateForm
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory


@method_decorator(staff_member_required, name="dispatch")
class CategoryListView(ListView):
    model = Category

    context_object_name = "categories"
    template_name = "recipe/category/list_view.html"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Category.objects.filter(name__icontains=query)
        return Category.objects.all()


@method_decorator(staff_member_required, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "recipe/category/delete_confirm.html"
    success_url = reverse_lazy("recipe:category_list")


@method_decorator(staff_member_required, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    template_name = "recipe/category/create_form.html"
    form_class = CategoryCreateForm
    success_url = reverse_lazy("recipe:category_list")


@method_decorator(staff_member_required, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "recipe/category/update_form.html"
    success_url = reverse_lazy("recipe:category_list")
    form_class = CategoryCreateForm


@method_decorator(staff_member_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    template_name = "recipe/product/create_form.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy("recipe:product_list")


@method_decorator(staff_member_required, name="dispatch")
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "recipe/product/list_view.html"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()


@method_decorator(staff_member_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "recipe/product/delete_confirm.html"
    success_url = reverse_lazy("recipe:product_list")


@method_decorator(staff_member_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    template_name = "recipe/product/update_form.html"
    success_url = reverse_lazy("recipe:product_list")
    form_class = ProductCreateForm
