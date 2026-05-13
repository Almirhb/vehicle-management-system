from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("user", "created_at")


class NotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"