from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsInstitutionOfficer
from .models import Vehicle
from .serializers import VehicleSerializer
from .services import (
    create_vehicle_for_user,
    submit_vehicle_for_approval,
    approve_vehicle,
    reject_vehicle,
    block_vehicle,
    deactivate_vehicle,
    is_institution_user,
)


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Vehicle.objects.select_related("owner").all().order_by("-created_at")

        if is_institution_user(user):
            return qs

        return qs.filter(owner=user)

    def perform_create(self, serializer):
        create_vehicle_for_user(self.request.user, serializer)

    @action(detail=False, methods=["get"], url_path="my")
    def my_vehicles(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user).order_by("-created_at")
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="submit-for-approval")
    def submit_for_approval(self, request, pk=None):
        vehicle = self.get_object()

        try:
            vehicle = submit_vehicle_for_approval(vehicle, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(vehicle).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="approve",
    permission_classes=[IsInstitutionOfficer],
)
    def approve(self, request, pk=None):
        vehicle = self.get_object()
        notes = request.data.get("notes", "Vehicle approved.")

        try:
            vehicle = approve_vehicle(vehicle, request.user, notes)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(vehicle).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="reject",
    permission_classes=[IsInstitutionOfficer],
)
    def reject(self, request, pk=None):
        vehicle = self.get_object()
        notes = request.data.get("notes", "Vehicle rejected.")

        try:
            vehicle = reject_vehicle(vehicle, request.user, notes)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(vehicle).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="block",
    permission_classes=[IsInstitutionOfficer],
)
    def block(self, request, pk=None):
        vehicle = self.get_object()

        try:
            vehicle = block_vehicle(vehicle, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(vehicle).data)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        vehicle = self.get_object()

        try:
            vehicle = deactivate_vehicle(vehicle, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(vehicle).data)
        def destroy(self, request, *args, **kwargs):
            vehicle = self.get_object()

            if vehicle.owner != request.user and not request.user.is_superuser:
                return Response(
            {"detail": "You can only delete your own vehicles."},
            status=status.HTTP_403_FORBIDDEN,
        )

            if vehicle.status not in ["draft", "rejected"]:
               return Response(
            {"detail": "Only draft or rejected vehicles can be deleted."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        vehicle.delete()

        return Response(
        {"detail": "Vehicle deleted successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )