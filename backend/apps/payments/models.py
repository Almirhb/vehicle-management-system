from django.conf import settings
from django.db import models
from apps.obligations.models import Obligation
from core.utils import generate_reference
class Payment(models.Model):
    METHOD_CHOICES=(("card","Card"),("bank_transfer","Bank Transfer"),("cash","Cash"),("e_albania","e-Albania"))
    STATUS_CHOICES=(("initiated","Initiated"),("successful","Successful"),("failed","Failed"),("refunded","Refunded"))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="payments")
    obligation=models.ForeignKey(Obligation,on_delete=models.CASCADE,related_name="payments")
    transaction_reference=models.CharField(max_length=80,unique=True,default="",blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    method=models.CharField(max_length=30,choices=METHOD_CHOICES,default="card")
    provider_reference=models.CharField(max_length=120,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="initiated",db_index=True)
    paid_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.transaction_reference:
            self.transaction_reference=generate_reference("PAY")
        super().save(*args,**kwargs)
    class Meta:
        indexes=[models.Index(fields=["user","status"]),models.Index(fields=["created_at"])]
    def __str__(self):
        return f"{self.obligation.vehicle.plate_number} - {self.amount} - {self.status}"




