from django.contrib import admin
from comment.models import Comment
from django.utils.translation import gettext_lazy as _

from .models import Relocate, UserRelocate


class UserRelocateInline(admin.TabularInline):
    model = UserRelocate
    fields = (
        'checked',
        'flag',
        'note',
    )
    can_delete = False
    extra = 0  # Shows exactly 1 empty form
    max_num = 1  # Maximum number of forms (including existing)
    verbose_name = "My Note"  # Single item title
    verbose_name_plural = "My Notes"  # Plural title


class CommentInline(admin.TabularInline):
    model = Comment
    fields = (
        'content',
        'likes',
        'dislikes',
    )
    readonly_fields = (
        'content',
        'likes',
        'dislikes',
    )
    can_delete = False
    extra = 0


class VoteFilter(admin.SimpleListFilter):
    title = _("Vote")

    parameter_name = "upvotes"

    def lookups(self, request, model_admin):
        return [
            ("Yes", _("Yes")),
            ("No", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.filter(upvotes__gt=0)
        if self.value() == "No":
            return queryset.filter(upvotes=0)


class CommentFilter(admin.SimpleListFilter):
    title = _("Comment")

    parameter_name = "comment"

    def lookups(self, request, model_admin):
        return [
            ("Yes", _("Yes")),
            ("No", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.filter(comment__isnull=False).distinct()
        if self.value() == "No":
            return queryset.filter(comment__isnull=True).distinct()
        

class CheckFilter(admin.SimpleListFilter):
    title = _("Check")

    parameter_name = "checked"

    def lookups(self, request, model_admin):
        return [
            ("Yes", _("Yes")),
            ("No", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.filter(userrelocate__checked=True).all()
        if self.value() == "No":
            return queryset.filter(userrelocate__checked=False).all()
        

class FlagFilter(admin.SimpleListFilter):
    title = _("Flag")

    parameter_name = "flag"

    def lookups(self, request, model_admin):
        return [
            ("Yes", _("Yes")),
            ("No", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.filter(userrelocate__flag=True).all()
        if self.value() == "No":
            return queryset.filter(userrelocate__flag=False).all()


class RelocateAdmin(admin.ModelAdmin):
    list_per_page = 10
    fields = (
        'job_url', 
        'upvotes',
        'text',
    )
    list_display = (
        'text',
    )
    readonly_fields = (
        'id',
        'job_url',
        'upvotes',
        'text'
    ) 
    search_fields = (
        'text',
    )
    inlines = [UserRelocateInline, CommentInline]
    list_filter = [VoteFilter, CommentFilter, CheckFilter, FlagFilter]

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context)
    

admin.site.register(Relocate, RelocateAdmin)

