from django.urls import path
from .views import RegisterView, EmailConfirmationView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verification/", EmailConfirmationView.as_view()),
]
