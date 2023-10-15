from django.shortcuts import render
from accounts.serialiser import *
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self,request):
        serialiser=UserRegistrationSerialiser(data=request.data)
        serialiser.is_valid(raise_exception=True)
        user=serialiser.save()
        token=get_tokens_for_user(user)
        
        return Response({"token":token,"message":"User Created Successfully"})