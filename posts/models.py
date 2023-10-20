from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.core.exceptions import ValidationError

User=get_user_model()

class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        
class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True,null=True)  # Add a field for the caption
    media = models.FileField(upload_to='post_media/',blank=True,null=True)  # Add a field for media files

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)