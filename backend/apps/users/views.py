from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) in ["institution_admin", "system_admin"] or user.is_superuser:
            return User.objects.all().order_by("-created_at")
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "change_password":
            return ChangePasswordSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user.role in ["institution_officer", "institution_admin", "system_admin"]:
            user.is_staff = True
            user.save(update_fields=["is_staff"])

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated], url_path="me")
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated], url_path="change-password")
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path="set-role")
    def set_role(self, request, pk=None):
        if not (request.user.is_superuser or getattr(request.user, "role", None) in ["institution_admin", "system_admin"]):
            return Response({"detail": "You do not have permission to change roles."}, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        role = request.data.get("role")
        allowed_roles = ["citizen", "institution_officer", "institution_admin", "system_admin"]

        if role not in allowed_roles:
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.is_staff = role in ["institution_officer", "institution_admin", "system_admin"] or user.is_superuser
        user.save(update_fields=["role", "is_staff"])

        return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })