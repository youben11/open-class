from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/django_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['open-class.org']
