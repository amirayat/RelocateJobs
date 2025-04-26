from django.db import models


class Relocate(models.Model):
    """
    linkedin relocate job model
    """
    job_url = models.URLField(unique=True, db_index=True)
    checked = models.BooleanField(default=False)
    gathered_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()