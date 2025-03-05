"""
Django settings for stationbook project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

FILE_UPLOAD_PERMISSIONS = 0o644

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_cleanup",
    "widget_tweaks",
    "hcaptcha_field",
    "accounts",
    "book",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "stationbook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "stationbook.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default=config("DATABASE_URL"))
}

CACHES = {
    "default": {
        "BACKEND": config("CACHE_BACKEND"),
        "LOCATION": config("CACHE_LOCATION"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = "Etc/UTC"

# URL base
SB_URL_BASE = config("SB_URL_BASE")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = os.path.join(SB_URL_BASE, 'static/')


LOGOUT_REDIRECT_URL = "home"

LOGIN_REDIRECT_URL = "home"

EMAIL_BACKEND = config("EMAIL_BACKEND")

LOGIN_URL = "login"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "maxBytes": 1024 * 1024 * 5,  # 5 Megabytes
            "backupCount": 25,
            "filename": os.path.join(BASE_DIR, "logs", "station_book.log"),
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "book": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": "INFO",
        },
    },
}

# Cache
CACHE_TIME_SHORT = config("CACHE_TIME_SHORT")
CACHE_TIME_MEDIUM = config("CACHE_TIME_MEDIUM")
CACHE_TIME_LONG = config("CACHE_TIME_LONG")
CACHE_TIME_LONG = config("CACHE_TIME_LONG")

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://orfeus-eu.org",
    "https://*.orfeus-eu.org",
    "http://127.0.0.1"
]

CSRF_COOKIE_HTTPONLY = config("CSRF_COOKIE_HTTPONLY")
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE")
SESSION_COOKIE_HTTPONLY = config("SESSION_COOKIE_HTTPONLY")
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE")

HCAPTCHA_SITEKEY = config("HCAPTCHA_SITEKEY")
HCAPTCHA_SECRET = config("HCAPTCHA_SECRET")
