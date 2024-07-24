from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.template.defaulttags import register
from recipe.models import Category, Product, Recipe, Diet
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from recipe.forms import CategoryCreateForm, ProductCreateForm, RecipeCreateForm, IngridientInlineFormSet, DietCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_system.models import UserPreference
from django.db.models import Q
from user_system.models import CustomUser
from recipe.mixins import UserIsOwnerMixin



@login_required(login_url="log_in/")
def create_recipe(request):
    recipe = Recipe()

    recipe_form = RecipeCreateForm(instance=recipe)

    formset = IngridientInlineFormSet(instance=recipe)

    if request.method == "POST":
        recipe_form = RecipeCreateForm(request.POST, request.FILES)

        formset = IngridientInlineFormSet(request.POST, request.FILES)
        if recipe_form.is_valid():
            created_recipe = recipe_form.save(commit=False)

            formset = IngridientInlineFormSet(
                request.POST, request.FILES, instance=created_recipe
            )

            for ing in formset.cleaned_data:
                
                if not ing['product'].piece_weight:
                    messages.error(request, "Ingridient can't be pieced")
                    context = {"recipe_form": recipe_form, "formset": formset}
                    return render(
                        template_name="recipe/recipe/create_form.html", context=context, request=request
                    )

            if formset.is_valid():
                created_recipe.author = request.user
                created_recipe.save()
                formset.save()
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
    paginate_by = 20

    def get_queryset(self):
        for_user = self.request.GET.get("user_filter")
        order = self.request.GET.get("order")
        search = self.request.GET.get("search")
        user = self.request.user
        query = Recipe.objects.all()
        if not user.is_anonymous:
            if for_user:
                user_pref = UserPreference.objects.get(user=user)
                recipes_for_user = Recipe.objects

                if for_user in ["hated", "all"]:
                    recipes_for_user = recipes_for_user.exclude(
                        Q(ingredients__product__category__in=user_pref.hate_categories.all())|
                        Q(ingredients__product__in=user_pref.hates_products.all())
                    )
                if for_user in ["favorite", "all"]:
                    recipes_for_user = recipes_for_user.filter(
                        Q(ingredients__product__category__in=user_pref.fav_categories.all()) |
                        Q(ingredients__product__in=user_pref.fav_products.all())
                    )
                query = recipes_for_user
        
        if search:
            query = query.filter(
                Q(title__icontains=search) |
                Q(ingredients__product__name__icontains=search)
            )
        
        if order and order != "revelant":
            orders = {
                "new": "-upload_date",
                "old": "upload_date"
            }
            query = query.order_by(orders[order])
        
        
        return query.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_text = self.request.GET.get('order')
        search_text = self.request.GET.get('search')
        context["order_text"] = order_text if order_text else ''
        context["search_text"] = search_text if search_text else ''
        return context


class UserRecipesListView(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = "recipe/recipe/user_recipes.html"
    context_object_name = "recipes"
    paginate_by = 20

    def get_queryset(self):
        for_user = self.request.GET.get("user_filter")
        order = self.request.GET.get("order")
        search = self.request.GET.get("search")
        user = self.request.user

        try:
            author=self.kwargs['pk']
        except:
            author=self.request.user
        
        query = Recipe.objects.filter(author= author)
        if not user.is_anonymous:
            if for_user:
                user_pref = UserPreference.objects.get(user=user)
                recipes_for_user = Recipe.objects

                if for_user in ["hated", "all"]:
                    recipes_for_user = recipes_for_user.exclude(
                        Q(ingredients__product__category__in=user_pref.hate_categories.all())|
                        Q(ingredients__product__in=user_pref.hates_products.all())
                    )
                if for_user in ["favorite", "all"]:
                    recipes_for_user = recipes_for_user.filter(
                        Q(ingredients__product__category__in=user_pref.fav_categories.all()) |
                        Q(ingredients__product__in=user_pref.fav_products.all())
                    )
                query = recipes_for_user
        
        if search:
            query = query.filter(
                Q(title__icontains=search) |
                Q(ingredients__product__name__icontains=search)
            )
        
        if order and order != "revelant":
            orders = {
                "new": "-upload_date",
                "old": "upload_date"
            }
            query = query.order_by(orders[order])
        
        
        return query.distinct()
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        order_text = self.request.GET.get('order')
        search_text = self.request.GET.get('search')

        try:
            user= CustomUser.objects.get(pk = self.kwargs['pk'])
        except:
            user=self.request.user

        context["order_text"] = order_text if order_text else ''
        context["search_text"] = search_text if search_text else ''
        context["user"] = user
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe/recipe/detail_view.html"
    context_object_name = "recipe"


class RecipeUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Recipe
    template_name = "recipe/recipe/update_form.html"
    success_url = reverse_lazy("recipe:recipe_list")
    form_class = RecipeCreateForm


class RecipeDeleteView(LoginRequiredMixin,UserIsOwnerMixin, DeleteView):
    model = Recipe
    template_name = "recipe/recipe/delete_confirm.html"
    success_url = reverse_lazy("recipe:recipe_list")


@method_decorator(staff_member_required, name="dispatch")
class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "recipe/category/list_view.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Category.objects.filter(name__icontains=query)
        return Category.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context["search_text"] = search_text if search_text else ''
        return context


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
    success_url = reverse_lazy("recipe:create_category")


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
    success_url = reverse_lazy("recipe:create_product")


@method_decorator(staff_member_required, name="dispatch")
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "recipe/product/list_view.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context["search_text"] = self.request.GET.get('search') if search_text else ''
        return context


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


@method_decorator(staff_member_required, name="dispatch")
class DietCreateView(CreateView):
    model = Diet
    template_name = "recipe/diet/create_form.html"
    form_class = DietCreateForm
    success_url = reverse_lazy("recipe:create_diet")


@method_decorator(staff_member_required, name="dispatch")
class DietListView(ListView):
    model = Diet
    context_object_name = "diets"
    template_name = "recipe/diet/list_view.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Diet.objects.filter(name__icontains=query)
        return Diet.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context["search_text"] = self.request.GET.get('search') if search_text else ''
        return context


@method_decorator(staff_member_required, name="dispatch")
class DietDetailView(ListView):
    model = Diet
    context_object_name = "diet"
    template_name = "recipe/diet/list_view.html"


@method_decorator(staff_member_required, name="dispatch")
class DietDeleteView(DeleteView):
    model = Diet
    template_name = "recipe/diet/delete_confirm.html"
    success_url = reverse_lazy("recipe:diet_list")


@method_decorator(staff_member_required, name="dispatch")
class DietUpdateView(UpdateView):
    model = Diet
    template_name = "recipe/diet/update_form.html"
    success_url = reverse_lazy("recipe:diet_list")
    form_class = DietCreateForm


@method_decorator(staff_member_required, name="dispatch")
class DietDetailView(DetailView):
    model = Diet
    template_name = "recipe/diet/detail_view.html"
    context_object_name = "diet"
