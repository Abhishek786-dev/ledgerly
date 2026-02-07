from rest_framework import viewsets, permissions
from .models import Account, PaymentMethod
from .serializers import AccountReadSerializer, PaymentMethodReadSerializer

# Create your views here.

class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentMethodView(viewsets.ModelViewSet):
    serializer_class = PaymentMethodReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
