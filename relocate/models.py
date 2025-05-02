from django.db import models
from django.contrib.auth.models import User


class Relocate(models.Model):
    """
    linkedin relocate job model
    """
    job_url = models.URLField(unique=True, db_index=True)
    gathered_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    text = models.TextField()
    active = models.BooleanField(default=True)
    published_on_linkedin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"


class UserRelocate(models.Model):
    """
    user relocate job model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relocate = models.ForeignKey(Relocate, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Tick to delete row, then save."

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'relocate'],
                name='user_relocate_unique_together'
            ),
        ]