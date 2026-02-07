from rest_framework import serializers
from .models import Vendor, Category

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'category_name', 'category_type', 'category_detail_type', 'is_active')
    
    def create(self, validated_data):
        # Attach logged-in user automatically
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VendorReadSerializer(serializers.ModelSerializer):
    default_category = CategoryReadSerializer(read_only=True)
    default_category_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Vendor
        fields = ('vendor_id', 'vendor_name', 'vendor_type', 'default_category', 'default_category_id', 'is_active')

    def create(self, validated_data):
        # Attach logged-in user automatically
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)