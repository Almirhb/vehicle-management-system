from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@permission_classes([AllowAny])
def mock_login(request):
    return Response(
        {
            "provider": "e-Albania",
            "status": "success",
            "message": "Mock OAuth login successful.",
            "user": {
                "identifier": "EA-USER-001",
                "full_name": "Mock Citizen",
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mock_payment(request):
    amount = request.data.get("amount")
    return Response(
        {
            "provider": "e-Albania",
            "status": "success",
            "message": "Mock payment processed successfully.",
            "amount": amount,
            "reference": "EA-PAY-0001",
        },
        status=status.HTTP_200_OK,
    )
