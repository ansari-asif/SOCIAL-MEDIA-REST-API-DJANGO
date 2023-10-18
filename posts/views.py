from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post,Like,Comment
from posts.serialiser import PostSerialiser,CommentSerialiser,LikeSerialiser


class PostList(APIView):
    def get(self,request):
        posts=Post.objects.all()
        serialiser=PostSerialiser(posts,many=True)
        return Response(serialiser.data)
    
    def post(self,request):
        serialiser=PostSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data,status=status.HTTP_201_CREATED)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)
    