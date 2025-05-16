from django.db import models



class OAUTH(models.Model):
    """
    linkedin oauth2 code model
    """
    code = models.TextField()