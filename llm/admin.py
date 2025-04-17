from django.contrib import admin
from .models import LLM


class LLMAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'name',
        'api_key',
    )

admin.site.register(LLM, LLMAdmin)


