"""Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# ruff: noqa: E501
import json
import os
from pathlib import Path
from typing import Any

import django_stubs_ext
from dotenv import load_dotenv

# get env vars from the `.env` file
load_dotenv(override=True)

# needed so that some specialized typing does not crash the app at runtime.
django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DJANGO_DEBUG", "0")))
SECURE_MODE = bool(int(os.getenv("DJANGO_SECURE_MODE", "0")))

# get some other config settings from the `.env` or actual environment
DJANGO_USE_CACHE = bool(int(os.getenv("DJANGO_USE_CACHE", "0")))
DJANGO_CSRF_TRUSTED_ORIGINS = json.loads(
    os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "[]")
)
DJANGO_ALLOWED_HOSTS = json.loads(os.getenv("DJANGO_ALLOWED_HOSTS", "[]"))
DJANGO_PROTECT_ADMIN = bool(int(os.getenv("DJANGO_PROTECT_ADMIN", "0")))

ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]
ALLOWED_HOSTS += DJANGO_ALLOWED_HOSTS

SECURE_PROXY = bool(int(os.getenv("DJANGO_SECURE_PROXY", "0")))

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "django_cotton",
    "lucide",
    "django_recaptcha",
    "solo",
    "django_tailwind_cli",
]

if DEBUG:
    INSTALLED_APPS.insert(
        0, "whitenoise.runserver_nostatic"
    )  # Prevent Django from handling static, whitenoise will do it
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

if DJANGO_PROTECT_ADMIN:
    MIDDLEWARE += ["app.middleware.IPAdminRestrictMiddleware"]

if DEBUG:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]


if DJANGO_USE_CACHE:
    MIDDLEWARE = [
        "django.middleware.cache.UpdateCacheMiddleware",
        *MIDDLEWARE,
        "django.middleware.cache.FetchFromCacheMiddleware",
    ]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# conditionally setup Postgres or SQLite depending on the .env setting.
# if 'DJANGO_USE_POSTGRES' is '1' we use Postgres otherwise use SQlite.
if bool(int(os.getenv("DJANGO_USE_POSTGRES", "0"))):
    db_config: dict[str, str | Path | int] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DJANGO_POSTGRES_DB", ""),
        "USER": os.getenv("DJANGO_POSTGRES_USER", ""),
        "PASSWORD": os.getenv("DJANGO_POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("DJANGO_POSTGRES_HOST", ""),
        "PORT": os.getenv("DJANGO_POSTGRES_PORT", ""),
        "CONN_MAX_AGE": 300,
        "CONN_HEALTH_CHECKS": True,
    }
else:
    db_config = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

DATABASES = {"default": db_config}


# Customize user model
AUTH_USER_MODEL = "app.UserProfile"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]

STATIC_ROOT = (
    os.getenv("DJANGO_STATIC_ROOT", "")
    if not DEBUG
    else str(BASE_DIR) + "/static"
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAILWIND_CLI_DIST_CSS = "css/site.css"

# Email Configuration
USE_LIVE_EMAIL = bool(int(os.getenv("USE_LIVE_EMAIL", "0")))

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if USE_LIVE_EMAIL
    else "django.core.mail.backends.console.EmailBackend"
)

# Email settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = bool(int(os.getenv("EMAIL_USE_TLS", "1")))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "webmaster@localhost")
CONTACT_FORM_RECIPIENT = os.getenv(
    "CONTACT_FORM_RECIPIENT", "admin@example.com"
)
EMAIL_TIMEOUT = 10

# Cache configuration for GitHub stats
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "max_pool_size": 4,
            "use_pooling": True,
        },
    }
}

# the below 3 settings are django defaults, you can modify as you prefer
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = int(os.getenv("DJANGO_CACHE_TIMEOUT", "600"))
CACHE_MIDDLEWARE_KEY_PREFIX = ""

# set django-solo to use the cache too
if DJANGO_USE_CACHE:
    SOLO_CACHE = "default"

# Settings for PRODUCTION.
# IMPORTANT! These require your site to be served over https. DONT enable this
# if it is not!!
if SECURE_MODE and not DEBUG:
    SECURE_HSTS_SECONDS = (
        30  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
        # 15552000 # use this AFTER you are sure all is good! This is 180 days!
    )
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    if SECURE_PROXY:
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
        USE_X_FORWARDED_HOST = True

    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_NAME = "__Secure-csrftoken"

    PERMISSIONS_POLICY: dict[str, list[Any]] = {
        "accelerometer": [],
        "ambient-light-sensor": [],
        "autoplay": [],
        "camera": [],
        "display-capture": [],
        "encrypted-media": [],
        "fullscreen": [],
        "geolocation": [],
        "gyroscope": [],
        "interest-cohort": [],
        "magnetometer": [],
        "microphone": [],
        "midi": [],
        "payment": [],
        "usb": [],
    }

# protect the admin route, only allow specific IP's to connect
# Only used if `DJANGO_PROTECT_ADMIN=1` in the environment
ADMIN_URL = "admin"
ADMIN_IPS_ALLOWED = json.loads(
    os.getenv("DJANGO_ADMIN_IPS_ALLOWED", '["127.0.0.1","localhost"]')
)
