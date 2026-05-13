from django.core.exceptions import PermissionDenied, ValidationError
from apps.notifications.services import create_notification
from apps.obligations.models import Obligation

INSTITUTION_ROLES = ["institution_officer", "institution_admin", "system_admin"]


def is_institution_user(user):
    return user.is_superuser or getattr(user, "role", None) in INSTITUTION_ROLES


def create_vehicle_for_user(user, serializer):
    vehicle = serializer.save(owner=user, status="draft")

    if vehicle.circulation_permit_expiry:
        Obligation.objects.create(
            vehicle=vehicle,
            obligation_type="tax",
            title="Rinovim i lejes së qarkullimit",
            description=f"Afati i lejes së qarkullimit për mjetin {vehicle.plate_number}.",
            due_date=vehicle.circulation_permit_expiry,
            amount="0.00",
            status="pending",
            external_reference=f"CIRC-{vehicle.id}",
        )

    if vehicle.road_tax_expiry:
        Obligation.objects.create(
            vehicle=vehicle,
            obligation_type="tax",
            title="Taksa vjetore e mjetit",
            description=f"Afati i taksës vjetore për mjetin {vehicle.plate_number}.",
            due_date=vehicle.road_tax_expiry,
            amount="120.00",
            status="pending",
            external_reference=f"TAX-{vehicle.id}",
        )

    if vehicle.inspection_expiry:
        Obligation.objects.create(
            vehicle=vehicle,
            obligation_type="inspection",
            title="Kolaudimi teknik",
            description=f"Afati i kolaudimit për mjetin {vehicle.plate_number}.",
            due_date=vehicle.inspection_expiry,
            amount="35.00",
            status="pending",
            external_reference=f"INSP-{vehicle.id}",
        )

    if vehicle.insurance_expiry:
        Obligation.objects.create(
            vehicle=vehicle,
            obligation_type="insurance",
            title="Siguracioni i mjetit",
            description=f"Afati i siguracionit për mjetin {vehicle.plate_number}.",
            due_date=vehicle.insurance_expiry,
            amount="250.00",
            status="pending",
            external_reference=f"INS-{vehicle.id}",
        )

    return vehicle

def submit_vehicle_for_approval(vehicle, user):
    if vehicle.owner != user and not user.is_superuser:
        raise PermissionDenied("You can only submit your own vehicle.")

    if vehicle.status not in ["draft", "rejected"]:
        raise ValidationError("Only draft or rejected vehicles can be submitted for approval.")

    vehicle.status = "pending_approval"
    vehicle.save(update_fields=["status"])

    create_notification(
        user=vehicle.owner,
        title="Vehicle submitted",
        message=f"Vehicle {vehicle.plate_number} was submitted for approval.",
    )

    return vehicle


def approve_vehicle(vehicle, officer, notes="Vehicle approved."):
    if not is_institution_user(officer):
        raise PermissionDenied("Only institution users can approve vehicles.")

    vehicle.status = "active"
    vehicle.save(update_fields=["status"])

    create_notification(
        user=vehicle.owner,
        title="Vehicle approved",
        message=f"Vehicle {vehicle.plate_number} has been approved.",
    )

    return vehicle


def reject_vehicle(vehicle, officer, notes="Vehicle rejected."):
    if not is_institution_user(officer):
        raise PermissionDenied("Only institution users can reject vehicles.")

    vehicle.status = "rejected"
    vehicle.save(update_fields=["status"])

    create_notification(
        user=vehicle.owner,
        title="Vehicle rejected",
        message=f"Vehicle {vehicle.plate_number} has been rejected. Reason: {notes}",
    )

    return vehicle


def block_vehicle(vehicle, officer):
    if not is_institution_user(officer):
        raise PermissionDenied("Only institution users can block vehicles.")

    vehicle.status = "blocked"
    vehicle.save(update_fields=["status"])

    create_notification(
        user=vehicle.owner,
        title="Vehicle blocked",
        message=f"Vehicle {vehicle.plate_number} has been blocked by the institution.",
    )

    return vehicle


def deactivate_vehicle(vehicle, user):
    if vehicle.owner != user and not is_institution_user(user):
        raise PermissionDenied("You do not have permission to deactivate this vehicle.")

    vehicle.status = "inactive"
    vehicle.save(update_fields=["status"])

    create_notification(
        user=vehicle.owner,
        title="Vehicle deactivated",
        message=f"Vehicle {vehicle.plate_number} has been deactivated.",
    )

    return vehicle