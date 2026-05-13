from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def health_check(request):
    return JsonResponse({"status": "ok", "message": "Vehicle Management System API is running."})


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/health/", health_check, name="api-health"),

    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/users/", include("apps.users.urls")),
    path("api/vehicles/", include("apps.vehicles.urls")),
    path("api/obligations/", include("apps.obligations.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/transactions/", include("apps.transactions.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),

    path("api/mock/", include("mock_api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
