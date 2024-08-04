from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, TemplateView
from django.template.defaulttags import register
from recipe.models import Category, Product, Recipe, Diet, RecipeIngridient
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


class MainMenuView(TemplateView):
    template_name = "recipe/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_recipes"] = Recipe.objects.all().order_by("-upload_date")[:6]
        return context


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
                
                if ing['product'].piece_weight == 0:
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
                return HttpResponseRedirect(reverse_lazy('recipe:recipe_list'))
    context = {"recipe_form": recipe_form, "formset": formset, "product_list": Product.objects.all()}
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
                query = user.preference.recipe_prefernce_filter(for_user)
        
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


class RecipeLike(UpdateView, LoginRequiredMixin):
    model = Recipe
    fields='__all__'

    def get_object(self):
        post_id = self.kwargs.get("pk")
        return get_object_or_404(Recipe, pk=post_id)

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        if user in recipe.likes.all():
            recipe.likes.remove(user)
        else:
            recipe.likes.add(user)
        recipe.save()
        return HttpResponseRedirect(request.POST.get('next', '/'))


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
                query = user.preference.recipe_prefernce_filter(for_user)

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
            user = CustomUser.objects.get(pk=self.kwargs['pk'])
        except:
            user = self.request.user

        context["order_text"] = order_text if order_text else ''
        context["search_text"] = search_text if search_text else ''
        context["user"] = user
        return context


class UserFavListView(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = "recipe/recipe/user_favorites.html"
    context_object_name = "recipes"
    paginate_by = 20

    def get_queryset(self):
        user = CustomUser.objects.get(pk=self.request.user.pk)
        for_user = self.request.GET.get("user_filter")
        query = user.favorite.all()
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")

        if not user.is_anonymous:
            if for_user:
                query = user.preference.recipe_prefernce_filter(for_user)

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
            user = CustomUser.objects.get(pk=self.kwargs['pk'])
        except:
            user = self.request.user

        context["order_text"] = order_text if order_text else ''
        context["search_text"] = search_text if search_text else ''
        context["user"] = user
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe/recipe/detail_view.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            if self.request.user.preference:
                user_pref = UserPreference.objects.get(user=self.request.user)
            else:
                user_pref = None
        else:
            user_pref = None
        if user_pref:
            fav_cat = user_pref.fav_categories.all()
            fav_prod = user_pref.fav_products.all()
            hate_cat = user_pref.hate_categories.all()
            hate_prod = user_pref.hates_products.all()
        else:
            fav_cat = fav_prod = hate_cat = hate_prod = None

        context["user_fav_cat"] = fav_cat
        context["user_fav_prod"] = fav_prod

        context["user_hate_cat"] = hate_cat
        context["user_hate_prod"] = hate_prod

        return context


class RecipeUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Recipe
    template_name = "recipe/recipe/update_form.html"
    success_url = reverse_lazy("recipe:recipe_list")
    form_class = RecipeCreateForm

    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = IngridientInlineFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        else:
            context['formset'] = IngridientInlineFormSet(
                instance=self.get_object()
            )

        context['img_rec'] = self.get_object().main_image

        return context

    def form_valid(self, form):
        ingredient_form = IngridientInlineFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        if ingredient_form.is_valid():
            self.object = form.save()
            ingredient_form.instance = self.get_object()
            for ing in ingredient_form.cleaned_data:
                try:
                    if ing['product'].piece_weight == 0:
                        messages.error(
                            self.request,
                            "Ingridient can't be pieced"
                        )
                        context = {
                            "recipe_form": form,
                            "formset": ingredient_form
                        }
                        return render(
                            template_name="recipe/recipe/update_form.html",
                            context=context,
                            request=self.request
                        )
                except:
                    pass

            ingredient_form.save()

        return super(RecipeUpdateView, self).form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Recipe
    template_name = "recipe/recipe/delete_confirm.html"
    success_url = reverse_lazy("recipe:recipe_list")


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
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context["search_text"] = search_text if search_text else ''
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
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Diet.objects.filter(name__icontains=query)
        return Diet.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context["search_text"] = search_text if search_text else ''
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
