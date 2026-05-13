from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Obligation
from .serializers import ObligationSerializer, ObligationStatusSerializer
from apps.payments.models import Payment
from apps.payments.services import process_payment

class ObligationViewSet(viewsets.ModelViewSet):
    queryset = Obligation.objects.select_related("owner", "vehicle").all().order_by("-created_at")
    permission_classes = [IsAuthenticated]
    serializer_class = ObligationSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Obligation.objects.select_related("vehicle").all().order_by("-created_at")

        if user.is_superuser or getattr(user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]:
            return qs

        return qs.filter(vehicle__owner=user)

    def perform_create(self, serializer):
        vehicle = serializer.validated_data.get("vehicle")
        owner = serializer.validated_data.get("owner") or getattr(vehicle, "owner", None)
        serializer.save(owner=owner, generated_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_obligations(self, request):
        qs = Obligation.objects.filter(owner=request.user).order_by("-created_at")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="mark-paid")
    def mark_paid(self, request, pk=None):
        obligation = self.get_object()

        if not (request.user.is_superuser or obligation.owner == request.user or getattr(request.user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        obligation.status = "paid"
        obligation.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(obligation).data)

    @action(detail=False, methods=["post"], url_path="refresh-statuses")
    def refresh_statuses(self, request):
        if not (request.user.is_superuser or getattr(request.user, "role", None) in ["institution_officer", "institution_admin", "system_admin"]):
            return Response({"detail": "Only institution users can refresh statuses."}, status=status.HTTP_403_FORBIDDEN)

        today = timezone.now().date()
        updated = 0

        for obligation in Obligation.objects.exclude(status__in=["paid", "cancelled"]):
            if obligation.due_date < today and obligation.status != "overdue":
                obligation.status = "overdue"
                obligation.save(update_fields=["status", "updated_at"])
                updated += 1
            elif obligation.due_date >= today and (obligation.due_date - today).days <= 7 and obligation.status == "pending":
                obligation.status = "due_soon"
                obligation.save(update_fields=["status", "updated_at"])
                updated += 1

        return Response({"detail": f"{updated} obligation(s) updated."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path="pay")
    def pay(self, request, pk=None):
        obligation = self.get_object()

        if obligation.vehicle.owner != request.user and not request.user.is_superuser:
            return Response(
            {"detail": "You can only pay your own obligations."},
            status=status.HTTP_403_FORBIDDEN,
        )

        if obligation.status == "paid":
            return Response(
            {"detail": "This obligation is already paid."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        payment = Payment.objects.create(
            user=request.user,
            obligation=obligation,
            amount=obligation.amount,
            method=request.data.get("method", "card"),
            status="initiated",
        )

        payment = process_payment(
            payment=payment,
            user=request.user,
            provider_reference=request.data.get("provider_reference", "MOCK-FRONTEND-PAYMENT"),
        )

        return Response({
        "detail": "Payment completed successfully.",
        "payment_id": payment.id,
        "payment_reference": payment.transaction_reference,
        "obligation_status": payment.obligation.status,
        })