from django.contrib import admin
from django.urls import path,include
from accounts.views import UserRegistrationView


urlpatterns = [
    path('registration',UserRegistrationView.as_view(), name="registration"),
]