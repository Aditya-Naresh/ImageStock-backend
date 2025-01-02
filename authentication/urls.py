from django.urls import path
from .views import RegisterView, EmailConfirmationView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verification/", EmailConfirmationView.as_view()),
    path("login/", LoginView.as_view()),
]
