from django.urls import path
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path("login", LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
    path("signup", views.signup, name="signup"),
    path("verify/<uidb64>/<token>", views.verify, name="verify"),
    path("password_reset", PasswordResetView.as_view(from_email="noreply@secure-notes.de"), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),  
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete")
]