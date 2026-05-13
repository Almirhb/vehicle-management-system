from django.core.exceptions import PermissionDenied
from apps.notifications.services import create_notification


INSTITUTION_ROLES = ["institution_officer", "institution_admin", "system_admin"]


def is_institution_user(user):
    return user.is_superuser or getattr(user, "role", None) in INSTITUTION_ROLES


def upload_document(serializer, user):
    vehicle = serializer.validated_data.get("vehicle")

    if vehicle.owner != user and not is_institution_user(user):
        raise PermissionDenied("You can only upload documents for your own vehicle.")

    document = serializer.save(uploaded_by=user, verified=False)

    create_notification(
        user=vehicle.owner,
        title="Document uploaded",
        message=f"Document '{document.title}' was uploaded for vehicle {vehicle.plate_number}.",
    )

    return document


def approve_document(document, officer):
    if not is_institution_user(officer):
        raise PermissionDenied("Only institution users can approve documents.")

    document.verified = True
    document.save(update_fields=["verified"])

    create_notification(
        user=document.vehicle.owner,
        title="Document approved",
        message=f"Document '{document.title}' for vehicle {document.vehicle.plate_number} was approved.",
    )

    return document


def reject_document(document, officer):
    if not is_institution_user(officer):
        raise PermissionDenied("Only institution users can reject documents.")

    document.verified = False
    document.save(update_fields=["verified"])

    create_notification(
        user=document.vehicle.owner,
        title="Document rejected",
        message=f"Document '{document.title}' for vehicle {document.vehicle.plate_number} was rejected.",
    )

    return document