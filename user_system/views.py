from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from user_system.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, TemplateView
from user_system.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


template_root = "user_system/"


class UserCreateView(CreateView):
    model = CustomUser
    template_name = template_root + "auth/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("recipe:recipe_list")


class UserUpdateView(UpdateView):
    form_class = CustomUserUpdateForm
    model = CustomUser
    template_name = template_root + "auth/edit_view.html"
    success_url = reverse_lazy("user_system:settings")

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['form'] = CustomUserUpdateForm(instance=self.request.user)
        return context
    
    
class CustomLoginView(LoginView):
    template_name = template_root+"auth/log_in.html"


class CustomLogoutView(LogoutView, LoginRequiredMixin):
    next_page = "user_system:log_in"


class UserSettingsView(TemplateView, LoginRequiredMixin):
    template_name = template_root+"auth/settings.html"


