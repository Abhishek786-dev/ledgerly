import uuid
from django.conf import settings
from django.db import models


class Category(models.Model):

    CATEGORY_TYPE_CHOICES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('transfer', 'Transfer'),
    )

    CATEGORY_DETAIL_CHOICES = (
        ('essential', 'Essential'),
        ('discretionary', 'Discretionary'),
    )

    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True
    )

    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES)
    category_detail_type = models.CharField(
        max_length=20,
        choices=CATEGORY_DETAIL_CHOICES,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        unique_together = ('user', 'category_name', 'category_type')
        indexes = [
            models.Index(fields=['category_type']),
            models.Index(fields=['category_detail_type']),
        ]

    def __str__(self):
        return f"{self.category_name} ({self.category_type}, {self.category_detail_type})"

class Vendor(models.Model):

    VENDOR_TYPE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    vendor_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendors',
        null=True
    )

    vendor_name = models.CharField(max_length=100)
    
    vendor_type = models.CharField(
        max_length=20,
        choices=VENDOR_TYPE_CHOICES
    )

    default_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='default_vendors'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendors'
        unique_together = ('user','vendor_name', 'vendor_type', 'default_category')
        indexes = [
            models.Index(fields=['vendor_name']),
            models.Index(fields=['vendor_type']),
            models.Index(fields=['default_category']),
        ]

    def __str__(self):
        return f"{self.vendor_name} ({self.vendor_type})"