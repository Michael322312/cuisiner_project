from django import forms
from recipe.models import Category, Product, Recipe, RecipeIngridient, Diet
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
        'product': forms.Select(attrs={'class': 'prod_select'}),
        'weight': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'style': 'width:140%; min-width: 120px', 'placeholder': 'Weight'}),
        'weight_unit': forms.Select(attrs={'class': 'form-control', 'style': 'width: 50px'})
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
            "recipe_text": forms.Textarea(attrs={"class": "form-control"}),
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

        fields = ["name", "calories", "category", 'piece_weight']

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "piece_weight": forms.NumberInput(attrs={"class": "form-select", "placeholder": "Piece weight", 'type': 'number', 'min': '0',})
        }

        labels = {"name": "Name", "calories": "Calories (per 100 grams)", "piece_weight": 'Enter piece weight in grams (If product is countable)'}


class DietCreateForm(forms.ModelForm):
    class Meta:
        model = Diet

        fields = ["name","forriben_categories", "caloires_per_dish"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "forriben_categories": forms.SelectMultiple(attrs={"class": "form-control"}),
            "caloires_per_dish": forms.NumberInput(attrs={"class": "form-select", "min": 0})        }

        labels = {"forriben_categories": "Forriben categories (cmd button to select)", "caloires_per_dish": "Callories per dish (If diet needs low callories)"}