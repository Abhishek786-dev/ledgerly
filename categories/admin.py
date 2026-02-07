from django.contrib import admin
from .models import Category, Vendor

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category_name',
        'category_type',
        'category_detail_type',
        'is_active',
        'created_at'
    )

    list_filter = ('category_type', 'category_detail_type', 'is_active')
    search_fields = ('category_name',)
    ordering = ('-created_at',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vendor_name',
        'vendor_type',
        'default_category',
        'is_active',
        'created_at'
    )

    list_filter = ('vendor_type', 'is_active')
    search_fields = ('vendor_name',)
    ordering = ('-created_at',)


