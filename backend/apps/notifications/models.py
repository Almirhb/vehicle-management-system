from django.conf import settings
from django.db import models
class Notification(models.Model):
    CATEGORY_CHOICES=(("system","System"),("payment","Payment"),("obligation","Obligation"),("transaction","Transaction"),("document","Document"))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")
    category=models.CharField(max_length=30,choices=CATEGORY_CHOICES,default="system")
    title=models.CharField(max_length=120)
    message=models.TextField()
    is_read=models.BooleanField(default=False,db_index=True)
    action_url=models.CharField(max_length=255,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes=[models.Index(fields=["user","is_read"]),models.Index(fields=["created_at"])]



NOTIFICATION_TYPE_CHOICES = [
    ("vehicle_update", "Vehicle Update"),
    ("document_update", "Document Update"),
    ("obligation_alert", "Obligation Alert"),
    ("payment_update", "Payment Update"),
    ("transaction_update", "Transaction Update"),
    ("system_alert", "System Alert"),
]

STATUS_CHOICES = [
    ("unread", "Unread"),
    ("read", "Read"),
    ("archived", "Archived"),
]

