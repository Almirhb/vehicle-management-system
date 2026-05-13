""""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.vehicles.models import Vehicle
from apps.obligations.models import Obligation
from apps.payments.models import Payment
from apps.transactions.models import Transaction
from apps.documents.models import Document
from apps.notifications.models import Notification


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_summary(request):
    user = request.user

    vehicles = Vehicle.objects.filter(owner=user)
    obligations = Obligation.objects.filter(vehicle__owner=user)

    return Response({
        "total_vehicles": vehicles.count(),
        "active_vehicles": vehicles.filter(status="active").count(),
        "pending_transfer_vehicles": vehicles.filter(status="pending_transfer").count(),
        "sold_vehicles": vehicles.filter(status="sold").count(),
        "blocked_vehicles": vehicles.filter(status="blocked").count(),
        "total_obligations": obligations.count(),
        "pending_obligations": obligations.filter(status="pending").count(),
        "paid_obligations": obligations.filter(status="paid").count(),
        "overdue_obligations": obligations.filter(status="overdue").count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def institution_summary(request):
    user = request.user

    if not user.is_staff and not user.is_superuser:
        return Response({"detail": "Institution access required."}, status=403)

    return Response({
        "total_vehicles": Vehicle.objects.count(),
        "active_vehicles": Vehicle.objects.filter(status="active").count(),
        "pending_transfer_vehicles": Vehicle.objects.filter(status="pending_transfer").count(),
        "sold_vehicles": Vehicle.objects.filter(status="sold").count(),
        "blocked_vehicles": Vehicle.objects.filter(status="blocked").count(),
        "total_obligations": Obligation.objects.count(),
        "pending_obligations": Obligation.objects.filter(status="pending").count(),
        "paid_obligations": Obligation.objects.filter(status="paid").count(),
        "overdue_obligations": Obligation.objects.filter(status="overdue").count(),
        "total_payments": Payment.objects.count(),
        "total_transactions": Transaction.objects.count(),
        "total_documents": Document.objects.count(),
        "total_notifications": Notification.objects.count(),
    })

 """
from apps.vehicles.models import Vehicle
from apps.obligations.models import Obligation
from apps.payments.models import Payment
from apps.transactions.models import Transaction
from apps.documents.models import Document
from apps.notifications.models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.vehicles.models import Vehicle
from apps.obligations.models import Obligation
from apps.payments.models import Payment
from apps.notifications.models import Notification


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_summary(request):
    user = request.user

    vehicles = Vehicle.objects.filter(owner=user)
    obligations = Obligation.objects.filter(vehicle__owner=user)

    unpaid_amount = sum(o.amount for o in obligations.exclude(status="paid"))

    return Response({
        "total_vehicles": vehicles.count(),
        "active_vehicles": vehicles.filter(status="active").count(),
        "pending_transfers": vehicles.filter(status="pending_transfer").count(),
        "unpaid_obligations": str(unpaid_amount),
        "overdue_obligations": obligations.filter(status="overdue").count(),
        "pending_obligations": obligations.filter(status="pending").count(),
        "paid_obligations": obligations.filter(status="paid").count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vehicles(request):
    user = request.user

    vehicles = Vehicle.objects.filter(owner=user).order_by("-created_at")

    data = []
    for v in vehicles:
        data.append({
            "id": v.id,
            "plate_number": v.plate_number,
            "make": v.make,
            "model": v.model,
            "year": v.year,
            "color": v.color,
            "status": v.status,
            "inspection_expiry": v.inspection_expiry,
            "insurance_expiry": v.insurance_expiry,
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_obligations(request):
    obligations = Obligation.objects.filter(vehicle__owner=request.user).order_by("due_date")

    data = []
    for o in obligations:
        data.append({
            "id": o.id,
            "vehicle": o.vehicle.plate_number,
            "obligation_type": o.obligation_type,
            "title": o.title,
            "amount": str(o.amount),
            "due_date": o.due_date,
            "status": o.status,
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_payments(request):
    payments = Payment.objects.filter(obligation__vehicle__owner=request.user).order_by("-created_at")

    data = []
    for p in payments:
        data.append({
            "id": p.id,
            "vehicle": p.obligation.vehicle.plate_number,
            "obligation": p.obligation.title,
            "amount": str(p.amount),
            "status": p.status,
            "created_at": p.created_at,
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

    data = []
    for n in notifications:
        data.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at,
        })

    return Response(data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_recent_activity(request):
    obligations = Obligation.objects.filter(
        vehicle__owner=request.user
    ).select_related("vehicle").order_by("due_date")

    data = []

    for o in obligations:
        data.append({
            "type": "obligation",
            "title": o.title,
            "description": o.status,
            "amount": str(o.amount),
            "due_date": o.due_date,
            "vehicle": o.vehicle.plate_number,
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def institution_summary(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"detail": "Institution access required."},
                status=status.HTTP_403_FORBIDDEN,
        )

    total_vehicles = Vehicle.objects.count()

    pending_approvals = Vehicle.objects.filter(
        status="pending_approval"
    ).count()

    active_vehicles = Vehicle.objects.filter(
        status="active"
    ).count()

    blocked_vehicles = Vehicle.objects.filter(
        status="blocked"
    ).count()

    recent_pending = Vehicle.objects.filter(
        status="pending_approval"
    ).select_related("owner").order_by("-created_at")[:10]

    recent_data = []

    for vehicle in recent_pending:
        recent_data.append({
            "id": vehicle.id,
            "plate_number": vehicle.plate_number,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "owner": vehicle.owner.username if vehicle.owner else "Unknown",
            "created_at": vehicle.created_at,
            "status": vehicle.status,
        })

    return Response({
        "total_vehicles": total_vehicles,
        "pending_approvals": pending_approvals,
        "active_vehicles": active_vehicles,
        "blocked_vehicles": blocked_vehicles,
        "pending_list": recent_data,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def institution_pending_approvals(request):
    user = request.user

    if not user.is_staff and not user.is_superuser:
        return Response({"detail": "Institution access required."}, status=403)

    pending_vehicles = Vehicle.objects.select_related("owner").filter(
        status="pending_approval"
    ).order_by("-created_at")[:20]

    data = []

    for vehicle in pending_vehicles:
        data.append({
            "id": vehicle.id,
            "type": "vehicle_registration",
            "title": "New Vehicle Registration",
            "plate_number": vehicle.plate_number,
            "vehicle": f"{vehicle.year} {vehicle.make} {vehicle.model}",
            "owner": vehicle.owner.username,
            "status": vehicle.status,
            "created_at": vehicle.created_at,
        })
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vehicle_overview(request):
    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    data = []

    for vehicle in vehicles:
        obligations = Obligation.objects.filter(
            vehicle=vehicle
        ).order_by("due_date")

        data.append({
            "id": vehicle.id,
            "plate_number": vehicle.plate_number,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "status": vehicle.status,
            "circulation_permit_expiry": vehicle.circulation_permit_expiry,
            "road_tax_expiry": vehicle.road_tax_expiry,
            "inspection_expiry": vehicle.inspection_expiry,
            "insurance_expiry": vehicle.insurance_expiry,
            "obligations": [
                {
                    "id": obligation.id,
                    "title": obligation.title,
                    "status": obligation.status,
                    "amount": str(obligation.amount),
                    "due_date": obligation.due_date,
                }
                for obligation in obligations
            ],
        })

    
    return Response(data)