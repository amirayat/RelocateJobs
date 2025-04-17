from django.db import models
from django.utils.translation import gettext_lazy as _


class LLM(models.Model):
    """
    LLM API credentials
    """
    name = models.TextField(unique=True)
    api_key = models.TextField(unique=True)

    class Meta:
        verbose_name = _("LLM")
        verbose_name_plural = _("LLM")