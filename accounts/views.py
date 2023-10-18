from django.shortcuts import render
from accounts.serialiser import *
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
    
class UserLoginView(APIView):
    def post(self,request):
        serialser=UserLoginSerialiser(data=request.data)
        serialser.is_valid(raise_exception=True)
        email=serialser.data.get('email')
        password=serialser.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({"token":token,"message":"Login Successfully"})
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}})

class UserPrfileView(APIView):
    
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializers=UserProfileSerializer(request.user)
        return Response(serializers.data,status=status.HTTP_200_OK)