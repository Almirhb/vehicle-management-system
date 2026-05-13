from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vehicle_check(request):
    plate_number = request.data.get("plate_number")
    vin = request.data.get("vin")

    return Response(
        {
            "provider": "DPSHTRR",
            "status": "success",
            "vehicle_found": True,
            "data": {
                "plate_number": plate_number,
                "vin": vin,
                "registration_status": "active",
                "inspection_status": "valid",
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def inspection_check(request):
    plate_number = request.data.get("plate_number")

    return Response(
        {
            "provider": "DPSHTRR",
            "status": "success",
            "plate_number": plate_number,
            "inspection_status": "valid",
            "inspection_expiry": "2026-12-31",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sale_check(request):
    plate_number = request.data.get("plate_number")

    return Response(
        {
            "provider": "DPSHTRR",
            "status": "success",
            "plate_number": plate_number,
            "sale_allowed": True,
            "message": "Vehicle is eligible for mock ownership transfer.",
        },
        status=status.HTTP_200_OK,
    )
