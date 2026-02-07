import uuid
from django.conf import settings
from django.db import models


class Account(models.Model):

    ACCOUNT_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('bank', 'Bank Account'),
        ('credit', 'Credit Card'),
        ('wallet', 'Digital Wallet'),
        ('investment', 'Investment'),
    )

    account_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )

    account_name = models.CharField(max_length=100)

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES
    )

    opening_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    bank_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['account_type']),
        ]
        unique_together = ('user', 'account_name')

    def __str__(self):
        return f"{self.account_name} ({self.user.email})"

class PaymentMethod(models.Model):
    """
    Docstring for PaymentMethod
    Example:
    method_name	provider
    UPI	    GPay
    UPI	    PhonePe
    Card	Visa
    Card	MasterCard
    Cash	NULL
    """
    payment_method_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        null=True
    )

    method_name = models.CharField(
        max_length=50
    )

    provider = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_methods'
        unique_together = ('user', 'method_name', 'provider')
        indexes = [
            models.Index(fields=['method_name']),
            models.Index(fields=['provider']),
        ]

    def __str__(self):
        return f"{self.method_name} - {self.method_name} ({self.provider or 'N/A'})"