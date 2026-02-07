from rest_framework import viewsets, permissions
from .models import Category, Vendor
from .serializers import CategoryReadSerializer, VendorReadSerializer

# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategoryReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VendorView(viewsets.ModelViewSet):
    serializer_class = VendorReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vendor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
