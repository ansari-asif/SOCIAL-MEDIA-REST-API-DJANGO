from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post,Like,Comment
from accounts.models import User
from posts.serialiser import PostSerialiser,PostListSerialiser,CommentSerialiser,LikeSerialiser,CommentSerializer_save,CommentSerialiser_add,UserSerializer,PostSerializer_for_comment,UserPostListSerialiser
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

class UserPostsView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):
        my_posts=Post.objects.filter(author=pk)
        serialiser=UserPostListSerialiser(my_posts,many=True)
        return Response(serialiser.data)
    
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
        return Response({"message":"Deleted successfully"},status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerialiser(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(uid=post_id)
            if post is not None:
                data = request.data.copy()
                data['post'] = post.uid
                data['author'] = request.user.id
                serializer = CommentSerialiser_add(data=data)
                if serializer.is_valid():
                    serializer.save()
                    author_data = UserSerializer(request.user).data
                    post_data = PostSerializer_for_comment(post).data
                    comment_data = serializer.data
                    comment_data['author'] = author_data
                    comment_data['post'] = post_data
                    return Response(comment_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid post id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('--------------------------------')
            print('Getting error ')
            print(e)
            print("--------------------------------")
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)       
        
class CommentDetail(APIView):
    permission_classes=[IsAuthenticated]
    def get_post(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
    def get_comment(self,pk,post_id):
        try:
            return Comment.objects.get(pk=pk,post=post_id)
        except Comment.DoesNotExist:
            return None
        
    def get(self, request, post_id, comment_id):
        try:           
            comment = self.get_comment(comment_id,post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerialiser(comment)
        return Response(serializer.data)

    def put(self, request, post_id, comment_id):
        try:
            comment = self.get_comment(comment_id,post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.POST.copy() 
        data['post']=comment.post.uid
        serializer = CommentSerializer_save(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        try:
            comment = self.get_comment(comment_id,post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if comment is not None:
            comment.delete()
            return Response({"message":"comment deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"comment not found."},status=status.HTTP_404_NOT_FOUND)


class LikeView(APIView):
    permission_classes =[IsAuthenticated]
    
    def post(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        user=request.user
        like=Like.objects.filter(user=user,post=post)
        if like :
            like.delete()
            return Response({"message":"You have unliked the post."},status=status.HTTP_200_OK)
        else:
            like=Like(user=user,post=post)
            like.save()
            return Response({"message":"You have liked the post."},status=status.HTTP_200_OK)
          