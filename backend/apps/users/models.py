from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("citizen", "Citizen"),
        ("institution_officer", "Institution Officer"),
        ("institution_admin", "Institution Admin"),
        ("system_admin", "System Admin"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
        ("pending_verification", "Pending Verification"),
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="citizen",
        db_index=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
    )

    national_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )

    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.national_id == "":
            self.national_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username