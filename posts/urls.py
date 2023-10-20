from django.contrib import admin
from django.urls import path,include
from posts.views import PostList,PostDetailsView


urlpatterns = [
    path('',PostList.as_view(), name="post"),
    path('<pk>',PostDetailsView.as_view(), name="post-details"),
]