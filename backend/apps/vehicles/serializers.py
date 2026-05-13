from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = (
            "owner",
            "created_at",
        )


class VehicleAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"