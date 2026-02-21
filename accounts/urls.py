from .views import RegisterView, LoginView, LogoutView, GoogleLogin
from django.urls import path


urlpatterns = [
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
