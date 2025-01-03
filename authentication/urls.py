from django.urls import path
from .views import (
    RegisterView,
    EmailConfirmationView,
    LoginView,
    ForgotPasswordView,
    SetNewPasswordView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verification/", EmailConfirmationView.as_view()),
    path("login/", LoginView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("set-password/", SetNewPasswordView.as_view()),
]
