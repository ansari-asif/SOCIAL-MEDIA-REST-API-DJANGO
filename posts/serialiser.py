from rest_framework import serializers
from posts.models import Comment,Like,Post
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email']
        
class PostSerializer_for_comment(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['uid','caption','media','created_at']
        
class CommentSerialiser(serializers.ModelSerializer):
    author = UserSerializer( read_only=True)
    post = PostSerializer_for_comment( read_only=True)
    class Meta:
        model=Comment
        fields="__all__"
        
class CommentSerialiser_add(serializers.ModelSerializer):
    # author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('uid', 'author', 'post', 'text', 'created_at')

class CommentSerializer_save(serializers.ModelSerializer):
    # author = UserSerializer( read_only=True)
    # post = PostSerializer_for_comment( read_only=True)
    class Meta:
        model=Comment
        fields = ('uid', 'author', 'post', 'created_at', 'updated_at', 'text')
    def validate(self,data):
        print('================================')
        print(data['author'])
        print(data['post'])
        print('================================')
        return data

        
class LikeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uid', 'author', 'post', 'created_at', 'updated_at', 'text')
        
class PostSerialiser(serializers.ModelSerializer):
    author = UserSerializer( read_only=True)
    comments = CommentSerialiser(many=True, read_only=True)

    class Meta:
        model=Post
        fields="__all__"
    def validate(self,data):
        if(data.get('media') is None and not data['caption']):
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
    comments = CommentSerialiser(many=True, read_only=True)
    class Meta:
        model=Post
        fields="__all__"


            
