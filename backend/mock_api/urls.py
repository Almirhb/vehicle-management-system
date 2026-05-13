from django.urls import path
from .e_albania_mock import mock_login, mock_payment
from .dpshtrr_mock import vehicle_check, inspection_check, sale_check

urlpatterns = [
    path("e-albania/login/", mock_login, name="mock-e-albania-login"),
    path("e-albania/payment/", mock_payment, name="mock-e-albania-payment"),
    path("dpshtrr/vehicle-check/", vehicle_check, name="mock-dpshtrr-vehicle-check"),
    path("dpshtrr/inspection/", inspection_check, name="mock-dpshtrr-inspection"),
    path("dpshtrr/sale/", sale_check, name="mock-dpshtrr-sale"),
]
