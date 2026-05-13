from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-only-change-me")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions",
    "django.contrib.messages","django.contrib.staticfiles","corsheaders","rest_framework",
    "rest_framework_simplejwt","drf_spectacular","apps.users","apps.vehicles","apps.obligations",
    "apps.payments","apps.transactions","apps.documents","apps.notifications","apps.dashboard",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "vehicle_system.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates","DIRS": [],"APP_DIRS": True,"OPTIONS": {"context_processors": [
    "django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "vehicle_system.wsgi.application"
ASGI_APPLICATION = "vehicle_system.asgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql","NAME": config("POSTGRES_DB", default="vehicle_system_db"),"USER": config("POSTGRES_USER", default="postgres"),"PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),"HOST": config("POSTGRES_HOST", default="localhost"),"PORT": config("POSTGRES_PORT", default="5432")}}
AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Tirane"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="http://localhost:3000").split(",")
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle","rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"user": "120/min","anon": "30/min"},
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),"REFRESH_TOKEN_LIFETIME": timedelta(days=7),"AUTH_HEADER_TYPES": ("Bearer",)}
SPECTACULAR_SETTINGS = {"TITLE": "Vehicle Management System API","DESCRIPTION": "Vehicle lifecycle platform with mock e-Albania and DPSHTRR integrations.","VERSION": "1.0.0"}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SECURE = False if DEBUG else True
