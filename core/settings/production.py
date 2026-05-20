from decouple import config

from .base import *


def parse_allowed_hosts(hosts_string):
    return [host.strip() for host in hosts_string.split(',')]


DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=parse_allowed_hosts)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
