from django.http import HttpResponse
from reportlab.pdfgen import canvas

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Payment.objects.select_related(
            "obligation",
            "obligation__vehicle",
            "user",
        ).order_by("-created_at")

        if user.is_superuser or user.is_staff:
            return qs

        return qs.filter(user=user)

    @action(detail=True, methods=["get"], url_path="receipt")
    def receipt(self, request, pk=None):
        payment = self.get_object()

        response = HttpResponse(content_type="application/pdf")

        response["Content-Disposition"] = (
            f'attachment; filename="receipt_{payment.transaction_reference}.pdf"'
        )

        p = canvas.Canvas(response)

        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, 800, "Vehicle Payment Receipt")

        p.setFont("Helvetica", 12)

        y = 760

        lines = [
            f"Receipt Reference: {payment.transaction_reference}",
            f"Vehicle: {payment.obligation.vehicle.plate_number}",
            f"Obligation: {payment.obligation.title}",
            f"Amount: ${payment.amount}",
            f"Method: {payment.method}",
            f"Status: {payment.status}",
            f"Paid At: {payment.paid_at}",
        ]

        for line in lines:
            p.drawString(50, y, line)
            y -= 30

        p.showPage()
        p.save()

        return response


    def get_queryset(self):
        user = self.request.user
        qs = Payment.objects.select_related(
            "user",
            "obligation",
            "obligation__vehicle",
        ).all().order_by("-created_at")

        if is_institution_user(user):
            return qs

        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_payments(self, request):
        payments = Payment.objects.select_related(
            "obligation",
            "obligation__vehicle",
        ).filter(user=request.user).order_by("-created_at")

        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="process")
    def process(self, request, pk=None):
        payment = self.get_object()
        provider_reference = request.data.get("provider_reference", "MOCK-PAYMENT")

        try:
            payment = process_payment(payment, request.user, provider_reference)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(payment).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="mark-failed",
    permission_classes=[IsAuthenticated]
)
    def mark_failed(self, request, pk=None):
        payment = self.get_object()
        provider_reference = request.data.get("provider_reference", "MOCK-FAILED")

        try:
            payment = mark_payment_failed(payment, request.user, provider_reference)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(payment).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="refund",
    permission_classes=[IsAuthenticated],
)
    def refund(self, request, pk=None):
        payment = self.get_object()

        try:
            payment = refund_payment(payment, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(payment).data)

    @action(detail=True, methods=["get"], url_path="receipt")
    def receipt(self, request, pk=None):
        payment = self.get_object()

        if payment.user != request.user and not is_institution_user(request.user):
            return Response({"detail": "You cannot view this receipt."}, status=status.HTTP_403_FORBIDDEN)

        return Response(build_receipt(payment))
    