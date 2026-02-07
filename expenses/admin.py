from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'account',
        'vendor',
        'category',
        'payment_method',
        'total_amount',
        'expense_date',
        'is_refund',
        'is_business'
    )
    list_filter = (
        'expense_date',
        'category',
        'vendor',
        'payment_method',
        'is_business',
        'is_refund',
    )
    search_fields = (
        'user__email',
        'account__account_name',
        'vendor__vendor_name',
        'notes'
    )
    ordering = ('-expense_date',)
    