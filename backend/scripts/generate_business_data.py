import os
import sys
import random
from decimal import Decimal
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vehicle_system.settings")
django.setup()

from apps.vehicles.models import Vehicle
from apps.obligations.models import Obligation
from apps.payments.models import Payment
from apps.notifications.models import Notification
from apps.transactions.models import Transaction
from apps.users.models import User


def random_due_date():
    today = timezone.now().date()
    return today + timedelta(days=random.randint(-30, 90))


def create_obligations():
    print("Creating obligations...")

    vehicles = Vehicle.objects.all()
    created = 0

    for vehicle in vehicles:
        obligation_types = [
            ("tax", "Annual Tax", Decimal("120.00")),
            ("inspection", "Technical Inspection", Decimal("35.00")),
            ("insurance", "Insurance Fee", Decimal("250.00")),
        ]

        for obligation_type, title, amount in obligation_types:
            if random.random() > 0.65:
                continue

            due_date = random_due_date()

            if due_date < timezone.now().date():
                status = "overdue"
            else:
                status = random.choice(["pending", "pending", "paid"])

            obligation = Obligation.objects.create(
                vehicle=vehicle,
                obligation_type=obligation_type,
                title=title,
                description=f"{title} for vehicle {vehicle.plate_number}",
                due_date=due_date,
                amount=amount,
                status=status,
                external_reference=f"OBL-{vehicle.id}-{obligation_type}-{random.randint(1000,9999)}",
            )

            created += 1

    print(f"Obligations created: {created}")


def create_payments():
    print("Creating payments...")

    obligations = Obligation.objects.all()
    created = 0

    for obligation in obligations:
        if obligation.status != "paid":
            continue

        if Payment.objects.filter(obligation=obligation).exists():
            continue

        Payment.objects.create(
            user=obligation.vehicle.owner,
            obligation=obligation,
            amount=obligation.amount,
            method=random.choice(["card", "bank_transfer", "e_albania"]),
            provider_reference=f"PROV-{random.randint(100000,999999)}",
            status="successful",
            paid_at=timezone.now() - timedelta(days=random.randint(1, 60)),
        )

        created += 1

    print(f"Payments created: {created}")


def create_notifications():
    print("Creating notifications...")

    created = 0

    for vehicle in Vehicle.objects.all():
        if vehicle.inspection_expiry and vehicle.inspection_expiry <= timezone.now().date() + timedelta(days=30):
            Notification.objects.create(
                user=vehicle.owner,
                title="Inspection reminder",
                message=f"Inspection for vehicle {vehicle.plate_number} expires soon.",
                is_read=random.choice([True, False]),
            )
            created += 1

        if vehicle.insurance_expiry and vehicle.insurance_expiry <= timezone.now().date() + timedelta(days=30):
            Notification.objects.create(
                user=vehicle.owner,
                title="Insurance reminder",
                message=f"Insurance for vehicle {vehicle.plate_number} expires soon.",
                is_read=random.choice([True, False]),
            )
            created += 1

    for obligation in Obligation.objects.filter(status="overdue"):
        Notification.objects.create(
            user=obligation.vehicle.owner,
            title="Overdue obligation",
            message=f"{obligation.title} for vehicle {obligation.vehicle.plate_number} is overdue.",
            is_read=random.choice([True, False]),
        )
        created += 1

    print(f"Notifications created: {created}")


def create_transfer_requests():
    print("Creating transfer requests...")

    users = list(User.objects.all())
    vehicles = list(Vehicle.objects.filter(status="active"))

    if len(users) < 2:
        print("Not enough users for transfer requests.")
        return

    created = 0

    sample_size = min(50, len(vehicles))

    for vehicle in random.sample(vehicles, sample_size):
        possible_buyers = [u for u in users if u != vehicle.owner]

        if not possible_buyers:
            continue

        new_owner = random.choice(possible_buyers)

        if Transaction.objects.filter(vehicle=vehicle, status="pending_review").exists():
            continue

        Transaction.objects.create(
            vehicle=vehicle,
            initiated_by=vehicle.owner,
            transaction_type="ownership_transfer",
            status="pending_review",
        )

        vehicle.status = "pending_transfer"
        vehicle.save(update_fields=["status"])

        Notification.objects.create(
            user=vehicle.owner,
            title="Transfer request created",
            message=f"Transfer request for vehicle {vehicle.plate_number} is pending review.",
            is_read=False,
        )

        created += 1

    print(f"Transfer requests created: {created}")


def main():
    create_obligations()
    create_payments()
    create_notifications()
    create_transfer_requests()
    print("Business data generation completed.")


if __name__ == "__main__":
    main()