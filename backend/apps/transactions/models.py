from django.conf import settings
from django.db import models
from apps.vehicles.models import Vehicle
from core.utils import generate_reference
class Transaction(models.Model):
    TYPE_CHOICES=(("sale","Sale"),("transfer","Transfer"),("inspection","Inspection"),("registration","Registration"))
    STATUS_CHOICES=(("pending","Pending"),("approved","Approved"),("rejected","Rejected"),("completed","Completed"))
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="transactions")
    initiated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="initiated_transactions")
    target_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="target_transactions")
    transaction_type=models.CharField(max_length=30,choices=TYPE_CHOICES)
    reference_code=models.CharField(max_length=80,unique=True,default="",blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    notes=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending",db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    approved_at=models.DateTimeField(null=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.reference_code:
            self.reference_code=generate_reference("TRX")
        super().save(*args,**kwargs)
    class Meta:
        indexes=[models.Index(fields=["vehicle","status"]),models.Index(fields=["transaction_type","status"])]


TRANSACTION_TYPE_CHOICES = [
    ("vehicle_registration", "Vehicle Registration"),
    ("ownership_transfer", "Ownership Transfer"),
    ("sale_request", "Sale Request"),
    ("status_change", "Status Change"),
    ("document_review", "Document Review"),
    ("obligation_update", "Obligation Update"),
    ("payment_event", "Payment Event"),
]

STATUS_CHOICES = [
    ("initiated", "Initiated"),
    ("pending_review", "Pending Review"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]
