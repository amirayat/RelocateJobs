from django.contrib import admin

from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    """
    contactus admin section
    """
    list_per_page = 10
    list_display = (
        'subject',
        'email',
        'created_at',
        'is_responsed',
    )
    readonly_fields = (
        'subject',
        'email',
        'created_at',
        'description'
    )
    list_filter = (
        'created_at',
    )
    exclude = (
        'is_responsed',
    )
    ordering = (
        'is_responsed',
        '-created_at',
    )
    search_fields = (
        'email',
        'subject',
        'description'
    )

    search_help_text = " Email, Subject, Description"

    


admin.site.register(ContactUs, ContactUsAdmin)
