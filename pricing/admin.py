from django.contrib import admin

from .models import Subscription, Deposite, Transaction, SiteWalletAddress


class DepositeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = (
        'created_at',
        'is_accepted'
    )
    ordering = (
        '-created_at',
    )
    list_display = (
        'id',
        'user',
        'amount',
        'created_at',
        'is_accepted'
    )
    search_fields = (
        'user__email',
        'user__id',
        'amount',
    )
    search_help_text = " Email, User ID, Amount"


class TransactionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = (
        'block_datetime',
    )
    ordering = (
        '-block_datetime',
    )
    list_display = (
        'id',
        'transaction_id',
        'block_datetime',
        '_from',
        'type',
        'value',
    )
    search_fields = (
        'transaction_id',
        '_from',
        'value',
    )
    search_help_text = " TXID, User Wallet Address, Transaction Value"


class SubscriptionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id',
        'user',
        'created_at',
    )
    search_fields = (
        'user__email',
    )
    ordering = (
        '-created_at',
    )
    search_help_text = " User Email"


admin.site.register(Deposite, DepositeAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SiteWalletAddress)
