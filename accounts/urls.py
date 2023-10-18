from django.contrib import admin
from django.urls import path,include
from accounts.views import UserRegistrationView,UserLoginView,UserPrfileView


urlpatterns = [
    path('registration',UserRegistrationView.as_view(), name="registration"),
    path('login',UserLoginView.as_view(), name="login"),
    path('profile',UserPrfileView.as_view(), name="profile"),
]