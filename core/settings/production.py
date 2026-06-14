from decouple import config

from .base import *


def parse_allowed_hosts(hosts_string):
    return [host.strip() for host in hosts_string.split(",")]


DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=parse_allowed_hosts)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# CORS — permite o frontend consumir a API
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=lambda origins_string: [origin.strip() for origin in origins_string.split(",")],
    default="",
)

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
