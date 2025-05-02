from django.shortcuts import redirect
from django.urls import path, reverse
from django.contrib import admin
from comment.models import Comment
from django.utils.html import format_html
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
            return queryset.filter(
                userrelocate__checked=True,
                userrelocate__user=request.user).all()
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
            return queryset.filter(
                userrelocate__flag=True, 
                userrelocate__user=request.user).all()
        if self.value() == "No":
            return queryset.filter(userrelocate__flag=False).all()


class RelocateAdmin(admin.ModelAdmin):
    list_per_page = 10
    fields = (
        'upvote_button',
        'job_url_clickable',
        'upvotes',
        'text',
    )
    list_display = (
        'text',
    )
    readonly_fields = (
        'upvote_button',
        'job_url_clickable',
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
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:id>/upvote/', self.process_upvote, name='upvote_url'),
        ]
        return custom_urls + urls
    
    def process_upvote(self, request, id):
        relocate = self.get_object(request, id)
        relocate.upvotes += 1
        relocate.save()
        redirect_url = "admin:{}_{}_change".format(self.opts.app_label, self.opts.model_name)
        return redirect(reverse(redirect_url, args=[id]))

    def upvote_button(self, obj):
        url = reverse('admin:upvote_url', kwargs={'id': obj.id})
        return format_html(
            '<a class="btn btn-outline-gray-600 d-inline-flex align-items-center" '
            'href="{}"><i class="fa fa-arrow-circle-up"></i>&nbsp; UpVote</a>',
            url
        )
    upvote_button.short_description = "If you have received an interview offer for this role, please click Upvote"
    
    def job_url_clickable(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.job_url)
    job_url_clickable.short_description = 'Job URL'
    

admin.site.register(Relocate, RelocateAdmin)

