from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from user_system.forms import CustomUserCreationForm, CustomUserUpdateForm, UserPreferenceCreateForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, TemplateView
from user_system.models import CustomUser, UserPreference
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_system.mixins import RequestUserIsUserMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from recipe.models import Recipe



template_root = "user_system/"


class UserCreateView(CreateView):
    model = CustomUser
    template_name = template_root + "auth/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("user_system:log_in")


class UserUpdateView(LoginRequiredMixin, RequestUserIsUserMixin, UpdateView):
    form_class = CustomUserUpdateForm
    model = CustomUser
    template_name = template_root + "auth/edit_view.html"
    success_url = reverse_lazy("user_system:settings")

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['form'] = CustomUserUpdateForm(instance=self.request.user)
        return context


class ResetPasswordView(SuccessMessageMixin,PasswordResetView):
    template_name = template_root + 'auth/mail/password_reset.html'
    email_template_name = template_root + 'auth/mail/password_reset_email.html'
    subject_template_name = template_root+ 'auth/mail/password_reset_subject'
    success_message = "We've sent you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('recipe:recipe_list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.template_name = template_root + 'auth/mail/password_reset.html'
        else:
            self.template_name = template_root + 'auth/mail/password_reset_nolog.html'
        
        return super().get(request, *args, **kwargs)

    
class CustomLoginView(LoginView):
    template_name = template_root + "auth/log_in.html"

    
class DeleteUserView(LoginRequiredMixin, RequestUserIsUserMixin, DeleteView):
    model = CustomUser
    template_name = template_root + "auth/delete_user.html"
    success_url = reverse_lazy("recipe:recipe_list")

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.check_password(self.request.POST.get('password')):
            get_user = CustomUser.objects.get(pk=user.pk)
            if get_user:
                get_user.delete()
                messages.success(self.request, "User succesfully deleted")
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(self.request, "User not found")
        else:
            messages.error(self.request, "Password didn't match")
        return render(request, self.template_name)
        

class CustomLogoutView(LogoutView, LoginRequiredMixin):
    next_page = "user_system:log_in"


class UserSettingsView(TemplateView, LoginRequiredMixin):
    template_name = template_root+"auth/settings.html"


class UserPreferenceCreateView(LoginRequiredMixin, CreateView):
    model = UserPreference
    template_name = template_root + "pref/create_view.html"
    form_class = UserPreferenceCreateForm
    success_url = reverse_lazy("recipe:recipe_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.model.objects.filter(user=self.request.user).exists():
            return redirect("user_system:edit_pref", pk=self.model.objects.filter(user=self.request.user).first().pk)
        else:
            return super().get(*args, **kwargs)



class UserPreferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPreference
    template_name = template_root + "pref/create_view.html"
    form_class = UserPreferenceCreateForm
    success_url = reverse_lazy("recipe:recipe_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.model.objects.filter(user=self.request.user).exists():
            return super().get(*args, **kwargs)
        else:
            return redirect("user_system:create_pref")


class UserFavorite(UpdateView, LoginRequiredMixin):
    model = CustomUser
    fields='__all__'

    def get_object(self):
        recipe_id = self.kwargs.get("pk")
        return get_object_or_404(Recipe, pk=recipe_id)

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        if recipe in user.favorite.all():
            user.favorite.remove(recipe)
        else:
            user.favorite.add(recipe)
        user.save()
        return HttpResponseRedirect(request.POST.get('next', '/'))

