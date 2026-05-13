from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source="vehicle.plate_number", read_only=True)
    uploaded_by_username = serializers.CharField(source="uploaded_by.username", read_only=True)

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = (
            "uploaded_by",
            "verified",
            "created_at",
        )


class DocumentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("verified",)