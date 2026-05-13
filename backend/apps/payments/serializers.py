from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(
        source="obligation.vehicle.plate_number",
        read_only=True,
    )

    obligation_title = serializers.CharField(
        source="obligation.title",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "vehicle_plate",
            "obligation_title",
            "transaction_reference",
            "amount",
            "method",
            "status",
            "paid_at",
            "created_at",
        ]