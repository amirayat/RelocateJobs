from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    """
    Comment under a Job post, with support for likes/dislikes and replies.
    """
    job = models.ForeignKey('relocate.Relocate', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
