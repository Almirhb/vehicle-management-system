from django.db import models

from apps.vehicles.models import Vehicle
class Obligation(models.Model):
    TYPE_CHOICES=(("tax","Annual Tax"),("inspection","Inspection"),("insurance","Insurance"),("penalty","Penalty"))
    STATUS_CHOICES=(("pending","Pending"),("paid","Paid"),("overdue","Overdue"),("cancelled","Cancelled"))
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="obligations")
    obligation_type=models.CharField(max_length=30,choices=TYPE_CHOICES)
    title=models.CharField(max_length=120)
    description=models.TextField(blank=True)
    due_date=models.DateField(db_index=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending",db_index=True)
    external_reference=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes=[models.Index(fields=["vehicle","status"]),models.Index(fields=["due_date","status"])]
    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.title} - {self.amount}"

OBLIGATION_TYPE_CHOICES = [
    ("registration_fee", "Registration Fee"),
    ("road_tax", "Road Tax"),
    ("inspection_fee", "Inspection Fee"),
    ("insurance_fee", "Insurance Fee"),
    ("traffic_fine", "Traffic Fine"),
    ("transfer_fee", "Transfer Fee"),
    ("other", "Other"),
]

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("due_soon", "Due Soon"),
    ("overdue", "Overdue"),
    ("paid", "Paid"),
    ("cancelled", "Cancelled"),
    ("disputed", "Disputed"),
]
