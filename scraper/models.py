from django.db import models
from django.utils.translation import gettext_lazy as _


class Linkedin(models.Model):
    """
    linkedin config
    """
    li_at_cookie = models.TextField(unique=True)

    class Meta:
        verbose_name = _("Linkedin")
        verbose_name_plural = _("Linkedin")