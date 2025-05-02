from django.db import models


class ActiveJobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)
    

class Job(models.Model):
    """
    linkedin job model
    """
    job_id = models.CharField(max_length=10, unique=True, db_index=True)
    checked = models.BooleanField(default=False)
    relocation = models.BooleanField(default=False)
    gathered_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    # Default manager
    objects = ActiveJobManager()
    # Include all objects manager
    all_objects = models.Manager()


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
