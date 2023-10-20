from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post,Like,Comment
from accounts.models import User
from posts.serialiser import PostSerialiser,PostListSerialiser,CommentSerialiser,LikeSerialiser
from rest_framework.permissions import IsAuthenticated


class PostList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        posts=Post.objects.all()
        serialiser=PostListSerialiser(posts,many=True)
        return Response(serialiser.data)
    
    def post(self,request):
        user=User.objects.get(pk=request.data.get('author'))
        serialiser=PostSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.validated_data['author'] = user
            serialiser.save()
            return Response(serialiser.data,status=status.HTTP_201_CREATED)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailsView(APIView):
    
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
        
    def get(self,request,pk):
        try:    
            post=self.get_object(pk)
            if post is not None:
                serialiser=PostSerialiser(post)
                return Response(serialiser.data,status=status.HTTP_200_OK)
            else:
                return Response({})
        except:
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerialiser(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)