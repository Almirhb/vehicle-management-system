from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .services import (
    create_overdue_obligation_notifications,
    create_inspection_expiry_notifications,
    create_insurance_expiry_notifications,
    create_due_soon_notifications,
)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.select_related("user").all().order_by("-created_at")

        if user.is_superuser or getattr(user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]:
            return qs

        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_notifications(self, request):
        qs = Notification.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()

        if notification.user != request.user and not request.user.is_superuser:
            return Response({"detail": "You can only update your own notification."}, status=status.HTTP_403_FORBIDDEN)

        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"detail": f"{updated} notification(s) marked as read."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="generate-overdue")
    def generate_overdue(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Institution access required."}, status=status.HTTP_403_FORBIDDEN)

        created = create_overdue_obligation_notifications()
        return Response({"created": created})

    @action(detail=False, methods=["post"], url_path="generate-inspection-reminders")
    def generate_inspection_reminders(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Institution access required."}, status=status.HTTP_403_FORBIDDEN)

        created = create_inspection_expiry_notifications()
        return Response({"created": created})

    @action(detail=False, methods=["post"], url_path="generate-insurance-reminders")
    def generate_insurance_reminders(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Institution access required."}, status=status.HTTP_403_FORBIDDEN)

        created = create_insurance_expiry_notifications()
        return Response({"created": created})
    @action(detail=False, methods=["post"], url_path="generate-due-soon")
    def generate_due_soon(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Institution access required."}, status=status.HTTP_403_FORBIDDEN)

        created = create_due_soon_notifications(days_before=10)
        return Response({"created": created}, status=status.HTTP_200_OK)