import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.email or self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    currency = models.CharField(max_length=3, default='INR')

    profile = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Profile"

class SocialAccount(models.Model):
    PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('github', 'GitHub'),
        ('facebook', 'Facebook'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_accounts'
    )

    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    provider_uid = models.CharField(max_length=255)

    email = models.EmailField()
    extra_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'provider_uid')
        indexes = [
            models.Index(fields=['provider']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.provider}"
    
    @property
    def is_social_user(self):
        return self.social_accounts.exists()