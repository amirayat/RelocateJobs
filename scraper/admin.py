from django.contrib import admin
from .models import Linkedin


class LinkedinAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'li_at_cookie',
    )

admin.site.register(Linkedin, LinkedinAdmin)


