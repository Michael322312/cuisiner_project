from django.urls import path
from user_system.views import UserCreateView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("log_in/", CustomLoginView.as_view(), name="log_in"),
    path("log_out/", CustomLogoutView.as_view(), name="log_out")
]

app_name = "user_system"
