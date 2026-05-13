from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionSerializer, TransactionDecisionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related(
        "vehicle", "initiated_by", "old_owner", "new_owner", "approved_by"
    ).all().order_by("-created_at")
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Transaction.objects.select_related(
            "vehicle", "initiated_by", "old_owner", "new_owner", "approved_by"
        ).all().order_by("-created_at")

        if user.is_superuser or getattr(user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]:
            return qs

        return qs.filter(initiated_by=user)

    def perform_create(self, serializer):
        serializer.save(initiated_by=self.request.user)

    @action(detail=False, methods=["post"], url_path="transfer-request")
    def transfer_request(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vehicle = serializer.validated_data["vehicle"]
        if vehicle.owner != request.user and not request.user.is_superuser:
            return Response({"detail": "You can only request transfer for your own vehicle."}, status=status.HTTP_403_FORBIDDEN)

        transaction = serializer.save(
            initiated_by=request.user,
            old_owner=vehicle.owner,
            status="pending_review",
            transaction_type="ownership_transfer",
        )

        vehicle.status = "pending_transfer"
        vehicle.save(update_fields=["status", "updated_at"])

        return Response(self.get_serializer(transaction).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        if not (request.user.is_superuser or getattr(request.user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]):
            return Response({"detail": "Only institution users can approve transactions."}, status=status.HTTP_403_FORBIDDEN)

        transaction = self.get_object()
        transaction.status = "approved"
        transaction.approved_by = request.user
        transaction.decision_notes = request.data.get("decision_notes", "Approved.")
        transaction.save(update_fields=["status", "approved_by", "decision_notes", "updated_at"])

        return Response(self.get_serializer(transaction).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        if not (request.user.is_superuser or getattr(request.user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]):
            return Response({"detail": "Only institution users can reject transactions."}, status=status.HTTP_403_FORBIDDEN)

        transaction = self.get_object()
        transaction.status = "rejected"
        transaction.approved_by = request.user
        transaction.decision_notes = request.data.get("decision_notes", "Rejected.")
        transaction.save(update_fields=["status", "approved_by", "decision_notes", "updated_at"])

        return Response(self.get_serializer(transaction).data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        if not (request.user.is_superuser or getattr(request.user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]):
            return Response({"detail": "Only institution users can complete transactions."}, status=status.HTTP_403_FORBIDDEN)

        transaction = self.get_object()

        if transaction.status != "approved":
            return Response({"detail": "Only approved transactions can be completed."}, status=status.HTTP_400_BAD_REQUEST)

        transaction.status = "completed"
        transaction.save(update_fields=["status", "updated_at"])

        vehicle = transaction.vehicle
        if transaction.transaction_type == "ownership_transfer" and transaction.new_owner:
            vehicle.owner = transaction.new_owner
            vehicle.status = "transferred"
            vehicle.save(update_fields=["owner", "status", "updated_at"])

        return Response(self.get_serializer(transaction).data)
