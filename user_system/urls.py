from django.urls import path
from user_system.views import UserCreateView, CustomLoginView, CustomLogoutView, UserSettingsView, UserUpdateView, ChangePasswordView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("log_in/", CustomLoginView.as_view(), name="log_in"),
    path("log_out/", CustomLogoutView.as_view(), name="log_out"),
    path("settings/", UserSettingsView.as_view(), name='settings'),
    path("edit_user/<int:pk>", UserUpdateView.as_view(), name="update_user"),
    path("change_password/<int:pk>", ChangePasswordView.as_view(), name="change_password"),
]

app_name = "user_system"
