from .models import Job, Location, Search


def processed_jobs(request):
    return {'processed_jobs': Job.objects.filter(active=True).count()}


def relocation_jobs(request):
    return {'relocation_jobs': Job.objects.filter(active=True, relocation=True).count()}


def locations(request):
    return {'locations': Location.objects.count()}


def search_terms(request):
    return {'search_terms': Search.objects.count()}