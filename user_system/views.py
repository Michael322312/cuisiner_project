from django.shortcuts import render
from user_system.forms import CustomUserCreationForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from user_system.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


template_root = "user_system/"


class UserCreateView(CreateView):
    model = CustomUser
    template_name = template_root + "auth/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("recipe:recipe_list")


class CustomLoginView(LoginView):
    template_name = template_root+"auth/log_in.html"


class CustomLogoutView(LogoutView):
    next_page = "user_system:log_in"
