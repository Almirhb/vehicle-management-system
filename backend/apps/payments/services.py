from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from apps.notifications.services import create_notification


INSTITUTION_ROLES = ["institution_officer", "institution_admin", "system_admin"]


def is_institution_user(user):
    return user.is_superuser or getattr(user, "role", None) in INSTITUTION_ROLES


def process_payment(payment, user, provider_reference="MOCK-PAYMENT"):
    if payment.user != user and not user.is_superuser:
        raise PermissionDenied("You can only pay your own payment record.")

    if payment.status == "successful":
        raise ValidationError("Payment is already successful.")

    payment.status = "successful"
    payment.provider_reference = provider_reference
    payment.paid_at = timezone.now()
    payment.save(update_fields=["status", "provider_reference", "paid_at"])

    obligation = payment.obligation
    obligation.status = "paid"
    obligation.save(update_fields=["status"])

    create_notification(
        user=payment.user,
        title="Payment successful",
        message=f"Payment {payment.transaction_reference} was completed successfully.",
    )

    return payment


def mark_payment_failed(payment, user, provider_reference="MOCK-FAILED"):
    if not is_institution_user(user):
        raise PermissionDenied("Only institution users can mark payments as failed.")

    payment.status = "failed"
    payment.provider_reference = provider_reference
    payment.save(update_fields=["status", "provider_reference"])

    create_notification(
        user=payment.user,
        title="Payment failed",
        message=f"Payment {payment.transaction_reference} failed.",
    )

    return payment


def refund_payment(payment, user):
    if not is_institution_user(user):
        raise PermissionDenied("Only institution users can refund payments.")

    if payment.status != "successful":
        raise ValidationError("Only successful payments can be refunded.")

    payment.status = "refunded"
    payment.save(update_fields=["status"])

    create_notification(
        user=payment.user,
        title="Payment refunded",
        message=f"Payment {payment.transaction_reference} was refunded.",
    )

    return payment


def build_receipt(payment):
    return {
        "receipt_number": payment.transaction_reference,
        "payer": payment.user.username,
        "vehicle": payment.obligation.vehicle.plate_number,
        "obligation": payment.obligation.title,
        "amount": str(payment.amount),
        "method": payment.method,
        "status": payment.status,
        "provider_reference": payment.provider_reference,
        "paid_at": payment.paid_at,
        "created_at": payment.created_at,
    }