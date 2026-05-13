import os
import sys
import random
import string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import pandas as pd
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vehicle_system.settings")
django.setup()

from apps.users.models import User
from apps.vehicles.models import Vehicle


CSV_PATH = "data/vehicles.csv"


def random_plate():
    return (
        random.choice(["AA", "AB", "AC", "AD", "TR", "DR"])
        + str(random.randint(100, 999))
        + random.choice(string.ascii_uppercase)
        + random.choice(string.ascii_uppercase)
    )


def random_vin():
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(17))


def random_engine():
    return "ENG-" + "".join(random.choice(string.digits) for _ in range(8))


def main():
    print("Loading CSV...")

    df = pd.read_csv(CSV_PATH)

    owners = list(User.objects.all())

    if not owners:
        print("No users found.")
        return

    created = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            owner = random.choice(owners)

            plate = random_plate()

            while Vehicle.objects.filter(plate_number=plate).exists():
                plate = random_plate()

            vin = random_vin()

            while Vehicle.objects.filter(vin=vin).exists():
                vin = random_vin()

            full_name = str(row["name"])

            parts = full_name.split(" ", 1)

            make = parts[0]

            if len(parts) > 1:
                model = parts[1]
            else:
                model = "Unknown"

            year = int(row["year"])

            market_value = float(row["selling_price"])

            vehicle = Vehicle.objects.create(
                owner=owner,
                plate_number=plate,
                vin=vin,
                make=make[:80],
                model=model[:80],
                year=year,
                color=random.choice(
                    [
                        "Black",
                        "White",
                        "Silver",
                        "Blue",
                        "Red",
                        "Gray",
                    ]
                ),
                registration_date="2024-01-01",
                inspection_expiry="2026-01-01",
                insurance_expiry="2026-01-01",
                engine_number=random_engine(),
                status=random.choice(
                    [
                        "active",
                        "active",
                        "active",
                        "pending_transfer",
                        "blocked",
                    ]
                ),
                market_value=market_value,
            )

            created += 1

            print(f"Created vehicle: {vehicle.plate_number}")

        except Exception as e:
            skipped += 1
            print(f"Skipped row: {e}")

    print("\nDONE")
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    main()