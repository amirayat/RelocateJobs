from django.utils import timezone
from datetime import timedelta
from .models import Relocate


# Calculate the cutoff date (1 month ago)
one_month_ago = timezone.now() - timedelta(days=31)

def deactivate_relocates():
    # Update all jobs older than 1 month to active=False
    Relocate.objects.filter(
        gathered_at__lt=one_month_ago,  # Jobs gathered before the cutoff
        active=True  # Only update currently active jobs
        ).update(active=False)