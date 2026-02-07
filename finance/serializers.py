from rest_framework import serializers
from .models import Account, PaymentMethod
from finance.models import PaymentMethod


class AccountReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'account_name', 'account_type', 'bank_name', 'current_balance', 'opening_balance', 'is_active')
    
    def create(self, validated_data):
        # Attach logged-in user automatically
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PaymentMethodReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('payment_method_id', 'method_name', 'provider', 'is_active')
    
    def create(self, validated_data):
        # Attach logged-in user automatically
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

