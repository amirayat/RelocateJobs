from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    """
    Comment under a Job post, with support for likes/dislikes and replies.
    """
    job = models.ForeignKey('relocate.Relocate', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date = self.created_at.strftime("%Y-%m-%d")
        return f"Commented on {date}"
