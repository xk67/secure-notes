from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from . import views

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
    path("signup", views.signup, name="signup"),
    path("verify/<token>", views.verify, name="verify"),
    path("password_reset", PasswordResetView.as_view(from_email="noreply@secure-notes.de", template_name="users/password_reset_form.html", email_template_name="users/password_reset_email.html", success_url=reverse_lazy("users:password_reset_done")), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", success_url=reverse_lazy("users:password_reset_complete")), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete', views.delete, name='delete_account'),
]
