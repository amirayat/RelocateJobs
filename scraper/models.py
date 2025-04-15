from django.db import models


class Linkedin(models.Model):
    """
    linkedin config
    """
    li_at_cookie = models.TextField()