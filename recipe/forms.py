from django import forms
from recipe.models import Category, Product, Recipe, RecipeIngridient
from django.forms import inlineformset_factory


IngridientInlineFormSet = inlineformset_factory(
    Recipe,
    RecipeIngridient,
    fields=(
        "product",
        "weight",
        "weight_unit",
    ),
    extra=1,
    widgets={
        'product': forms.Select(attrs={'class': ''}),
        'weight': forms.NumberInput(attrs={'class': '', 'type': 'number', 'min': '0',}),
        'weight_unit': forms.Select(attrs={'class': ''})
    },
    labels={
        'product': '',
        'weight': '',
        'weight_unit': ''
    }
)


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngridient
        fields = ["product", "weight", "weight_unit"]


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe

        fields = ["title", "main_image", "url_yt_video", "introduction", "recipe_text"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "main_image": forms.FileInput(attrs={"class": "form-control"}),
            "url_yt_video": forms.TextInput(
                attrs={"class": "form-control", "type": "url"}
            ),
            "introduction": forms.TextInput(attrs={"class": "form-control"}),
            "recipe_text": forms.TextInput(attrs={"class": "form-control"}),
        }


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ["name"]

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}

        labels = {
            "name": "Category name",
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = ["name", "calories", "category"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

        labels = {"name": "Name", "calories": "Calories (per 100 grams)"}
