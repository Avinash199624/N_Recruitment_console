"""
Django settings for neeri_recruitment_portal project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import Csv, config
from rest_framework import ISO_8601
from datetime import timedelta
from corsheaders.defaults import default_headers
import environ
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

def absolute(*relative):\
    return os.path.join(BASE_DIR, *relative)

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5j2jm!c)k71h=udcrwh=nkd4b752if8^#kiw9kxt_bvwajho4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'knox',
    'corsheaders',
    'user',
    'document',
    'communication_template',
    'job_posting',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
AUTOCREATE_VALID_SSL_USERS = True

ROOT_URLCONF = 'neeri_recruitment_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'neeri_recruitment_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neeri-live-local',
        'USER': 'postgres',
        'PASSWORD': 'Admin@123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_TLS = True
EMAIL_PORT = '587'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
AUTH_KEY = env('AUTH_KEY')
SMS_SENDER_ID = env('SMS_SENDER_ID')
ROUTE = env('ROUTE')
COUNTRY_CODE = env('COUNTRY_CODE')

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = ["neeri_recruitment_portal.backends.EmailOrUsernameModelBackend"]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = (
    absolute('static'),
)

# STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Session settings
# https://docs.djangoproject.com/en/2.2/ref/settings/#sessions

SESSION_COOKIE_AGE = config(
    "SESSION_COOKIE_AGE", default=12096000, cast=int
)  # Approximately 2 weeks, in seconds
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME", default="sessionid")
SESSION_COOKIE_HTTPONLY = config("SESSION_COOKIE_HTTPONLY", default=True, cast=bool)
SESSION_COOKIE_SAMESITE = config("SESSION_COOKIE_SAMESITE", default="Lax")
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
SESSION_EXPIRE_AT_BROWSER_CLOSE = config(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", default=False, cast=bool
)

# CSRF settings
# https://docs.djangoproject.com/en/2.2/ref/settings/#security

CSRF_COOKIE_AGE = config(
    "CSRF_COOKIE_AGE", default=31449600, cast=int
)  # Approximately 1 year, in seconds
CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN", default=None)
CSRF_COOKIE_NAME = config("CSRF_COOKIE_NAME", default="csrftoken")
CSRF_COOKIE_HTTPONLY = config("CSRF_COOKIE_HTTPONLY", default=False, cast=bool)
CSRF_COOKIE_SAMESITE = config("CSRF_COOKIE_SAMESITE", default="Lax")
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
CSRF_USE_SESSIONS = config("CSRF_USE_SESSIONS", default=False, cast=bool)
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

REST_FRAMEWORK = {
    # Define which type of auth to use by default
    "DEFAULT_AUTHENTICATION_CLASSES": ["knox.auth.TokenAuthentication"],
    # Default permission to use on all our views
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"]

}

REST_KNOX = {
    # Cryptography used to secure token
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    # Time until token expire
    "TOKEN_TTL": timedelta(days=7),
    # Number max of tokens that a user can have. 'None' means no limit
    "TOKEN_LIMIT_PER_USER": None,
    # RESERVED: we should limit number of tokens pre user in future
    # "TOKEN_LIMIT_PER_USER": 5,
    # Should the token expiry time be extended when used?
    "AUTO_REFRESH": False,
    "EXPIRY_DATETIME_FORMAT": ISO_8601,
}
CORS_ORIGIN_ALLOW_ALL = config("CORS_ORIGIN_ALLOW_ALL", default=True, cast=bool)
CORS_REPLACE_HTTPS_REFERER = config(
    "CORS_REPLACE_HTTPS_REFERER", default=False, cast=bool
)
CORS_ALLOW_CREDENTIALS = config("CORS_ALLOW_CREDENTIALS", default=False, cast=bool)
CORS_ALLOW_HEADERS = list(default_headers) + config(
    "CORS_ALLOW_HEADERS", default="", cast=Csv()
)
CORS_EXPOSE_HEADERS = config("CORS_EXPOSE_HEADERS", default="", cast=Csv())
CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", default="", cast=Csv())
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://shreyastechnosoft.centralindia.cloudapp.azure.com",
    "https://neeri-findinpi.vercel.app"
]
CORS_ORIGIN_REGEX_WHITELIST = config(
    "CORS_ORIGIN_REGEX_WHITELIST", default="", cast=Csv()
)
# BASE_URL = 'https://20.198.86.180:8181'
BASE_URL = 'http://20.198.86.180:8181'
