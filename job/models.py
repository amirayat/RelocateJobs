from django.db import models


class Job(models.Model):
    """
    linkedin job model
    """
    job_id = models.CharField(max_length=10, unique=True, db_index=True)
    checked = models.BooleanField(default=False)
    relocation = models.BooleanField(default=False)
