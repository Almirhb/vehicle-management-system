from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "role",
        "status",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    list_filter = (
        "role",
        "status",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "System Info",
            {
                "fields": (
                    "role",
                    "status",
                    "national_id",
                    "phone",
                    "address",
                    "email_verified",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "System Info",
            {
                "fields": (
                    "role",
                    "status",
                    "national_id",
                    "phone",
                    "address",
                    "email_verified",
                )
            },
        ),
    )