from rest_framework import serializers
from accounts.models import User


class UserRegistrationSerialiser(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=User
        fields=['email','name','tc','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self,attrs):
        password=attrs['password']
        password2=attrs['password2']
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    
    
class UserLoginSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email']