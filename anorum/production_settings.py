"""
Production Django settings for anorum project.
"""

import os

from anorum.shared_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "anorum.com",
    "www.anorum.com",
]


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRESQL_DBNAME"],
        "USER": os.environ["POSTGRESQL_USER"],
        "PASSWORD": os.environ["POSTGRESQL_PASSWORD"],
        "HOST": os.environ["POSTGRESQL_HOST"],
        "PORT": os.environ["POSTGRESQL_PORT"],
    }
}

SESSION_COOKIE_DOMAIN = ".anorum.com"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
