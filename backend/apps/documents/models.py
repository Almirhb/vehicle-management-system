from django.conf import settings
from django.db import models
from apps.vehicles.models import Vehicle


class Document(models.Model):
    TYPE_CHOICES = (
        ("registration", "Registration"),
        ("insurance", "Insurance"),
        ("inspection", "Inspection"),
        ("sale_contract", "Sale Contract"),
        ("other", "Other"),
    )

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=120)
    file = models.FileField(upload_to="documents/")
    expires_at = models.DateField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["vehicle", "document_type"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.title}"