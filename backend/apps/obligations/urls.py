from rest_framework.routers import DefaultRouter
from .views import ObligationViewSet

router = DefaultRouter()
router.register("", ObligationViewSet, basename="obligations")

urlpatterns = router.urls
