from django.db import models



class OAUTH(models.Model):
    """
    linkedin oauth2 code model
    """
    code = models.TextField()


class Token(models.Model):
    """
    linkedin oauth2 token model
    """
    access_token = models.TextField()
    refresh_token = models.TextField()