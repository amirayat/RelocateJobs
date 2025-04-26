from django.contrib import admin
from .models import Relocate


class RelocateAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'job_url',
        'checked',
        'gathered_at',
        'text'
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'checked',
    )

admin.site.register(Relocate, RelocateAdmin)

