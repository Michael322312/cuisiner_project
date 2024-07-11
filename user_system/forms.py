from django import forms
from user_system.models import CustomUser, UserPreference
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3 w-75 rounded", "autocomplete": "new-password", "placeholder": "Password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3 w-75 rounded", "autocomplete": "new-password", "placeholder": "Password confirmation"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("avatar", "intro", )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control mb-3 w-75 rounded", "placeholder": "Username"}),
            "avatar": forms.FileInput(attrs={"class": "form-control mb-3 w-75 rounded"}),
            "intro": forms.Textarea(attrs={"class": "form-control mb-3 w-75 rounded", "placeholder": "Bio", 'rows': "4;"}),
        }