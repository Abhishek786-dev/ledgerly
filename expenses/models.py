import uuid
from django.db import models
from django.conf import settings
from finance.models import Account, PaymentMethod
from categories.models import Category, Vendor

class Expense(models.Model):
    """
    Docstring for Expense
    Use UUID PK → public-safe, unguessable.
    Money fields → DecimalField, max_digits=15, decimal_places=2.
    Index user_id, account_id, expense_date → fast reporting.
    Soft deletion / flags optional via is_active (not strictly necessary if you track refunds).
    FK constraints → use PROTECT or SET_NULL where deleting related rows is dangerous.
    tax_amount	DecimalField	Track taxes separately for business / GST purposes.
    is_recurring	BooleanField	Mark if this is a recurring expense (for subscriptions, rent, etc.)
    recurring_interval	CharField	'weekly', 'monthly', 'yearly', if is_recurring=True. Useful for automation.
    receipt	FileField / URLField	Store or link receipts for audit / expense verification.
    location	CharField	Optional GPS location / city for expense (useful for travel reporting).
    tags	JSONField / ManyToMany	Optional tags for filtering / advanced analytics (e.g., "team lunch", "client expense").
    reference_id	CharField	Optional external transaction ID from bank/UPI/credit card. Useful for reconciliation.
    reconciled	Boolean	Whether this expense has been reconciled with account statements.
    """
    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='expenses')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='expenses')
    
    expense_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    notes = models.TextField(null=True, blank=True)
    is_refund = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    
    is_recurring = models.BooleanField(default=False)
    recurring_interval = models.CharField(max_length=20, null=True, blank=True)
    
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    tags = models.JSONField(null=True, blank=True)
    reference_id = models.CharField(max_length=100, null=True, blank=True)
    reconciled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expenses'
        indexes = [
            models.Index(fields=['user', 'expense_date']),
            models.Index(fields=['account']),
            models.Index(fields=['vendor']),
            models.Index(fields=['category']),
            models.Index(fields=['is_business']),
            models.Index(fields=['is_recurring']),
        ]
        ordering = ['-expense_date']

    def __str__(self):
        return f"{self.user.email} - {self.total_amount} on {self.expense_date}"
