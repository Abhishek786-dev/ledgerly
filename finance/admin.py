from django.contrib import admin
from .models import Account, PaymentMethod


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'account_name',
        'user',
        'account_type',
        'current_balance',
        'is_active',
        'created_at'
    )

    list_filter = ('account_type', 'is_active')
    search_fields = ('account_name', 'bank_name', 'user__email')
    ordering = ('-created_at',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        'method_name',
        'user',
        'provider',
        'is_active',
        'created_at'
    )

    list_filter = ('method_name', 'is_active')
    search_fields = ('method_name', 'provider')
    ordering = ('method_name',)