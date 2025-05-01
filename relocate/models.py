from django.db import models
from django.contrib.auth.models import User


class Relocate(models.Model):
    """
    linkedin relocate job model
    """
    job_url = models.URLField(unique=True, db_index=True)
    checked = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    gathered_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class UserRelocate(models.Model):
    """
    user relocate job model
    """
    relocate = models.ForeignKey(Relocate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=True)
    flag = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)