from django.urls import path
from .views import (
    user_summary,
    user_vehicles,
    user_obligations,
    user_payments,
    user_notifications,
    user_recent_activity,
    user_vehicle_overview,
    institution_summary,
)

urlpatterns = [
    path("user-summary/", user_summary, name="user-summary"),
    path("user-vehicles/", user_vehicles, name="user-vehicles"),
    path("user-obligations/", user_obligations, name="user-obligations"),
    path("user-payments/", user_payments, name="user-payments"),
    path("user-notifications/", user_notifications, name="user-notifications"),
    path("user-recent-activity/", user_recent_activity, name="user-recent-activity"),
    path("user-vehicle-overview/", user_vehicle_overview, name="user-vehicle-overview"),
    path("institution-summary/", institution_summary, name="institution-summary"),
]