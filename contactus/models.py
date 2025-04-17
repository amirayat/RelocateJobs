from django.db import models


class ContactUs(models.Model):
    """
    contact us model
    """
    subject = models.CharField(max_length=60)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responsed = models.BooleanField(default=False)
    response = models.TextField(null=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
