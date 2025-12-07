from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView

urlpatterns = [
    path("login", LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
    path("signup", SignUpView.as_view(template_name="users/signup.html"), name="signup")
]