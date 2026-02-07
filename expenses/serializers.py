from rest_framework import serializers
from .models import Expense
from finance.serializers import AccountReadSerializer, PaymentMethodReadSerializer
from categories.serializers import VendorReadSerializer, CategoryReadSerializer



class ExpenseSerializer(serializers.ModelSerializer):
    # READ (nested)
    account = AccountReadSerializer(read_only=True)
    vendor = VendorReadSerializer(read_only=True)
    payment_method = PaymentMethodReadSerializer(read_only=True)
    category = CategoryReadSerializer(read_only=True)

    # WRITE (IDs)
    account_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True)
    vendor_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    payment_method_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    class Meta:
        model = Expense
        fields = (
            "expense_id",
            # read-only fields
            "user",
            "account",
            "vendor",
            "category",
            # write-only fields
            'account_id',
            'vendor_id',
            'payment_method_id',
            'category_id',

            "payment_method",
            "total_amount",
            "expense_date",
            "is_refund",
            "is_business",
            "is_recurring",
            "recurring_interval",
            "receipt",
            "location",
            "tags",
            "reference_id",
            "reconciled",
            "notes",
            "tax_amount",
            "created_at",
        )
        
        read_only_fields = ('id', 'user', 'created_at')
    
    def create(self, validated_data):
        # Attach logged-in user automatically
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

