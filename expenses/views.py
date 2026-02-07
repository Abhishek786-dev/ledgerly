from rest_framework import viewsets, permissions
from .models import Expense, Category, Account
from .serializers import ExpenseSerializer


class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related('account', 'vendor', 'payment_method')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
