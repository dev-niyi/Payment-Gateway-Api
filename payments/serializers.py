from rest_framework import serializers
from .models import Payment

class PaymentSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['reference', 'status', 'created_at']