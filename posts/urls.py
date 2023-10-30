from django.contrib import admin
from django.urls import path,include
from posts.views import PostList,PostDetailsView,CommentList,CommentDetail,UserPostsView,LikeView


urlpatterns = [
    path('comments/<post_id>/', CommentList.as_view(), name='comment-list'),
    path('comments/<str:post_id>/<str:comment_id>', CommentDetail.as_view(), name='comment-detail'),
    path('',PostList.as_view(), name="post"),
    path('<pk>',PostDetailsView.as_view(), name="post-details"),
    path('<post_id>/like',LikeView.as_view(), name="post-like"),
    path('user-wise/<pk>',UserPostsView.as_view(), name="user-wise-post-list"),
]