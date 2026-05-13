from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, current_user

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = router.urls + [
    path("me/", current_user, name="current-user"),
]
