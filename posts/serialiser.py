from rest_framework import serializers
from posts.models import Comment,Like,Post
from accounts.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email']
    
class CommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"
        
class LikeSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields="__all__"

class PostSerialiser(serializers.ModelSerializer):
    author = UserSerializer( read_only=True)

    class Meta:
        model=Post
        fields="__all__"
    def validate(self,data):
        if(data['media'] is None and not data['caption']):
            raise serializers.ValidationError("caption or media should not be empty")
        return data
    
    def validate_media(self,data): 
        if data is not None:    
            if data.size > 4 * 1024 * 1024:
                raise serializers.ValidationError("File size is too large, should under 5MB.")
            if not data.content_type.startswith('image'):
                raise serializers.ValidationError("Invalid file format. Only images are allowed.")
        return data
            
class PostListSerialiser(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 
    class Meta:
        model=Post
        fields="__all__"
            
