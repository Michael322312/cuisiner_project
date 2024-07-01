from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.core.paginator import Paginator
from django.template.defaulttags import register
from recipe.models import Category, Product, RecipeIngridient, Recipe
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from recipe.forms import CategoryCreateForm, ProductCreateForm, RecipeCreateForm, IngridientInlineFormSet
from django.http import HttpResponseRedirect


def create_recipe(request):
    recipe = Recipe()

    recipe_form = RecipeCreateForm(instance=recipe)  # setup a form for the parent

    formset = IngridientInlineFormSet(instance=recipe)

    if request.method == "POST":
        recipe_form = RecipeCreateForm(request.POST, request.FILES)

        formset = IngridientInlineFormSet(request.POST, request.FILES)
        if recipe_form.is_valid():
            created_recipe = recipe_form.save(commit=False)
            formset = IngridientInlineFormSet(
                request.POST, request.FILES, instance=created_recipe
            )

            if formset.is_valid():
                created_recipe.author = request.user
                created_recipe.save()
                formset.save()
                total_calories = created_recipe.calculate_total_calories()
                created_recipe.total_calories = total_calories
                created_recipe.save()
                return HttpResponseRedirect(reverse_lazy('recipe:category_list'))

    context = {"recipe_form": recipe_form, "formset": formset}

    return render(
        template_name="recipe/recipe/create_form.html", context=context, request=request
    )



class RecipeListView(ListView):
    model = Recipe
    template_name = "recipe/recipe/list_view.html"
    context_object_name = "recipes"
    paginate_by = 10


@method_decorator(staff_member_required, name="dispatch")
class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "recipe/category/list_view.html"
    paginate_by = 10

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
    paginate_by = 10

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
