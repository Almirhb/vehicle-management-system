from django.utils import timezone

from apps.notifications.models import Notification
from apps.vehicles.models import Vehicle
from apps.obligations.models import Obligation


def create_notification(user, title, message):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        is_read=False,
    )


def create_overdue_obligation_notifications():
    today = timezone.now().date()
    obligations = Obligation.objects.filter(status="overdue")

    created = 0

    for obligation in obligations:
        Notification.objects.create(
            user=obligation.vehicle.owner,
            title="Overdue obligation",
            message=f"Your obligation '{obligation.title}' for vehicle {obligation.vehicle.plate_number} is overdue.",
            is_read=False,
        )
        created += 1

    return created


def create_inspection_expiry_notifications(days=30):
    today = timezone.now().date()
    limit_date = today + timezone.timedelta(days=days)

    vehicles = Vehicle.objects.filter(
        inspection_expiry__isnull=False,
        inspection_expiry__gte=today,
        inspection_expiry__lte=limit_date,
    )

    created = 0

    for vehicle in vehicles:
        Notification.objects.create(
            user=vehicle.owner,
            title="Inspection expiry reminder",
            message=f"Inspection for vehicle {vehicle.plate_number} expires on {vehicle.inspection_expiry}.",
            is_read=False,
        )
        created += 1

    return created


def create_insurance_expiry_notifications(days=30):
    today = timezone.now().date()
    limit_date = today + timezone.timedelta(days=days)

    vehicles = Vehicle.objects.filter(
        insurance_expiry__isnull=False,
        insurance_expiry__gte=today,
        insurance_expiry__lte=limit_date,
    )

    created = 0

    for vehicle in vehicles:
        Notification.objects.create(
            user=vehicle.owner,
            title="Insurance expiry reminder",
            message=f"Insurance for vehicle {vehicle.plate_number} expires on {vehicle.insurance_expiry}.",
            is_read=False,
        )
        created += 1

    return created


def create_transfer_update_notification(user, vehicle, status):
    return create_notification(
        user=user,
        title="Transfer update",
        message=f"Transfer status for vehicle {vehicle.plate_number}: {status}.",
    )


from datetime import timedelta
from django.utils import timezone
from apps.obligations.models import Obligation


def create_due_soon_notifications(days_before=10):
    today = timezone.now().date()
    target_date = today + timedelta(days=days_before)

    obligations = Obligation.objects.filter(
        due_date=target_date,
        status="pending",
    ).select_related("vehicle", "vehicle__owner")

    created = 0

    for obligation in obligations:
        already_exists = Notification.objects.filter(
            user=obligation.vehicle.owner,
            title="Afat pagese afër skadimit",
            message__icontains=obligation.vehicle.plate_number,
        ).exists()

        if already_exists:
            continue

        Notification.objects.create(
            user=obligation.vehicle.owner,
            title="Afat pagese afër skadimit",
            message=f"{obligation.title} për mjetin {obligation.vehicle.plate_number} skadon më {obligation.due_date}.",
            is_read=False,
        )

        created += 1

    return created