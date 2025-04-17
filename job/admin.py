from django.contrib import admin
from .models import Job, Location, Search


class JobAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'job_id',
        'checked',
        'relocation',
        'upvote',
        'gathered_at',
        'active',
    )
    search_fields = (
        'job_id',
    )

class LocationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'keyword',
    )

class SearchAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'keyword',
    )

admin.site.register(Job, JobAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Search, SearchAdmin)


