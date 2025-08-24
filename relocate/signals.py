from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector

from .models import Relocate


@receiver(post_save, sender=Relocate)
def update_search_vector(sender, instance, created, **kwargss):
    if created:  # Only for new records
        Relocate.objects.filter(pk=instance.pk).update(
            search_vector=SearchVector('text')
        )