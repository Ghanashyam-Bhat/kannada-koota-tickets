"""
Django settings for kannada_koota project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import json
import firebase_admin
from firebase_admin import credentials

load_dotenv()

# Initialize Firebase
FIREBASE_CRED = os.environ.get("FIREBASE_CRED")
cred = credentials.Certificate(json.loads(FIREBASE_CRED))
firebase_admin.initialize_app(cred)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vd#l&#$$+6h4f4cmzhwvv#%w(*-etbs(z+3r!x-+=dxk$vg!y@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# This is to configure the settnigs for serving static files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Reading Configuration File
configFile = {}
try:
    with open("./config.conf") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore empty lines and comments
                key, value = line.split("=", 1)
                configFile[key.strip()] = value.strip()
except:
    pass

ALLOWED_HOSTS = [
    # Removing http:// and https:// from host names
    "127.0.0.1",
    configFile["DJANGO"].split("//")[1],
    configFile["REACT_WEB"].split("//")[1],
]

CORS_ALLOWED_ORIGINS = [
    configFile["DJANGO"],
    configFile["REACT_WEB"],
]
CORS_ORIGIN_ALLOW_ALL = False
# Application definition


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_extensions",
    # User defined apps
    "ticket_generation.apps.TicketGenerationConfig",
    "authentication.apps.AuthenticationConfig",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "kannada_koota.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# WSGI_APPLICATION = "kannada_koota.wsgi.application"
WSGI_APPLICATION = "vercel_app.wsgi.app"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {"default": dj_database_url.config(default=os.environ.get("POSTGRES_URL"))}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CROSS ORIGIN REQUEST SETTINGS

CORS_ORIGIN_WHITELIST = [
    configFile["DJANGO"],
    configFile["REACT_WEB"],
]

CORS_ALLOW_HEADERS = [
    "Accept",
    "Accept-Encoding",
    "Authorization",
    "Content-Type",
    "Cookie",  # Add 'Cookie' header to allow
    "Origin",
]

CORS_ALLOWED_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
    # Add other allowed methods as needed
]


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_CREDENTIALS = True


SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_DOMAIN = ""
