from rest_framework import serializers
from .models import Obligation


class ObligationSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source="vehicle.plate_number", read_only=True)

    class Meta:
        model = Obligation
        fields = "__all__"


class ObligationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obligation
        fields = "__all__"