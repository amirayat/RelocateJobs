from django.db import models


class LLM(models.Model):
    """
    LLM API credentials
    """
    name = models.TextField(unique=True)
    api_key = models.TextField(unique=True)