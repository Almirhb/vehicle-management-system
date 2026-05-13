from django.conf import settings
from django.db import models
class Vehicle(models.Model):
    STATUS_CHOICES=(("active","Active"),("pending_transfer","Pending Transfer"),("sold","Sold"),("blocked","Blocked"))
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="vehicles")
    plate_number=models.CharField(max_length=20,unique=True)
    vin=models.CharField(max_length=50,unique=True)
    make=models.CharField(max_length=80)
    model=models.CharField(max_length=80)
    year=models.PositiveIntegerField()
    color=models.CharField(max_length=50,blank=True)
    registration_date = models.DateField()
    circulation_permit_expiry = models.DateField(null=True, blank=True)
    road_tax_expiry = models.DateField(null=True, blank=True)
    inspection_expiry = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    engine_number=models.CharField(max_length=50,blank=True)
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default="active",db_index=True)
    market_value=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes=[models.Index(fields=["owner","status"]),models.Index(fields=["inspection_expiry"]),models.Index(fields=["insurance_expiry"])]
    def __str__(self):
        return self.plate_number

STATUS_CHOICES = (
    ("draft", "Draft"),
    ("pending_approval", "Pending Approval"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("active", "Active"),
    ("pending_transfer", "Pending Transfer"),
    ("sold", "Sold"),
    ("blocked", "Blocked"),
    ("inactive", "Inactive"),
)



owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicles")
plate_number = models.CharField(max_length=20, unique=True)
vin = models.CharField(max_length=50, unique=True)
brand = models.CharField(max_length=100)
model = models.CharField(max_length=100)
year = models.PositiveIntegerField()
fuel_type = models.CharField(max_length=50)
color = models.CharField(max_length=50, blank=True, null=True)
registration_date = models.DateField()
circulation_permit_expiry = models.DateField(null=True, blank=True)
road_tax_expiry = models.DateField(null=True, blank=True)
inspection_expiry = models.DateField(null=True, blank=True)
insurance_expiry = models.DateField(null=True, blank=True)
status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="draft")
verification_notes = models.TextField(blank=True, null=True)
is_verified = models.BooleanField(default=False)


