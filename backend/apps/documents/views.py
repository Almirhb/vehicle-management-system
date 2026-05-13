from django.core.exceptions import PermissionDenied
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsInstitutionOfficer
from .models import Document
from .serializers import DocumentSerializer
from .services import (
    upload_document,
    approve_document,
    reject_document,
    is_institution_user,
)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Document.objects.select_related(
            "vehicle",
            "vehicle__owner",
            "uploaded_by",
        ).all().order_by("-created_at")

        if is_institution_user(user):
            return qs

        return qs.filter(vehicle__owner=user)

    def perform_create(self, serializer):
        upload_document(serializer, self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_documents(self, request):
        documents = Document.objects.select_related(
            "vehicle",
            "uploaded_by",
        ).filter(vehicle__owner=request.user).order_by("-created_at")

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(
    detail=True,
    methods=["post"],
    url_path="approve",
    permission_classes=[IsInstitutionOfficer],
)
    def approve(self, request, pk=None):
        document = self.get_object()

        try:
            document = approve_document(document, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(document).data)

    @action(
    detail=True,
    methods=["post"],
    url_path="reject",
    permission_classes=[IsInstitutionOfficer],
)
    def reject(self, request, pk=None):
        document = self.get_object()

        try:
            document = reject_document(document, request.user)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(document).data)

    @action(detail=True, methods=["get"], url_path="download-info")
    def download_info(self, request, pk=None):
        document = self.get_object()

        if document.vehicle.owner != request.user and not is_institution_user(request.user):
            return Response({"detail": "You cannot access this document."}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "id": document.id,
            "title": document.title,
            "file_url": document.file.url if document.file else None,
            "verified": document.verified,
        })