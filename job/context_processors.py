from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

from .models import Job, Location, Search


def processed_jobs(request):
    return {'processed_jobs': Job.objects.count()}


def relocation_jobs(request):
    return {'relocation_jobs': Job.objects.filter(active=True, relocation=True).count()}


def locations(request):
    return {'locations': Location.objects.count()}


def locations_list(request):
    return {'locations_list': Location.objects.all()}


def search_terms(request):
    return {'search_terms': Search.objects.count()}


def search_terms_list(request):
    return {'search_terms_list': Search.objects.all()}

# Use timezone-aware datetime
# includes today, so 9 days total
nine_days_ago = timezone.now().date() - timedelta(days=8)

def recent_9_days_jobs(request):
    return {'recent_9_days_jobs': Job.objects.filter(gathered_at__date__gte=nine_days_ago).count()}

def recent_9_days_relocations(request):
    return {'recent_9_days_relocations': Job.objects.filter(relocation=True,
                                                            gathered_at__date__gte=nine_days_ago).count()}

def recent_9_days_upvotes(request):
    return {'recent_9_days_upvotes': Job.objects.filter(gathered_at__date__gte=nine_days_ago).aggregate(sum=Sum('upvote'))['sum'] or 0}