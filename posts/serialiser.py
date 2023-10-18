from rest_framework import serializers
from posts.models import Comment,Like,Post


class CommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"
        
class LikeSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields="__all__"
        
class PostSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields="__all__"
