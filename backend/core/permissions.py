from rest_framework.permissions import BasePermission


class IsCitizen(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "citizen"


class IsInstitutionOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "institution_officer"
            or request.user.role == "institution_admin"
            or request.user.role == "system_admin"
            or request.user.is_superuser
        )


class IsInstitutionAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "institution_admin"
            or request.user.role == "system_admin"
            or request.user.is_superuser
        )


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "system_admin"
            or request.user.is_superuser
        )