from django.db import models


class Job(models.Model):
    """
    linkedin job model
    """
    job_id = models.CharField(max_length=10, unique=True, db_index=True)
    checked = models.BooleanField(default=False)
    relocation = models.BooleanField(default=False)
    gathered_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    """
    linkedin location model
    """
    keyword = models.CharField(max_length=32, unique=True, db_index=True)


class Search(models.Model):
    """
    linkedin search model
    """
    keyword = models.CharField(max_length=32, unique=True, db_index=True)
