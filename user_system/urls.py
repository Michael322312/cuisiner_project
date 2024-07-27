from django.urls import path

from user_system.views import (
    UserCreateView,
    CustomLoginView,
    CustomLogoutView,
    UserSettingsView,
    UserUpdateView,
    ResetPasswordView,
    DeleteUserView,
    UserPreferenceUpdateView,
    UserPreferenceCreateView
    
)


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("log_in/", CustomLoginView.as_view(), name="log_in"),
    path("log_out/", CustomLogoutView.as_view(), name="log_out"),
    path("settings/", UserSettingsView.as_view(), name='settings'),
    path("edit_user/<int:pk>", UserUpdateView.as_view(), name="update_user"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path("delete_user/<int:pk>", DeleteUserView.as_view(), name="delete_user"),
    path("preferences/", UserPreferenceCreateView.as_view(), name="create_pref"),
    path("preferences/<int:pk>", UserPreferenceUpdateView.as_view(), name="edit_pref"),



]

app_name = "user_system"
