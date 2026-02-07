from django.db import transaction
from .models import User

@transaction.atomic
def register_user(email, username, password):
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    return user