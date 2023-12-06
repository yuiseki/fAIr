"""
Django settings for aiproject project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.aiproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.aiproject.com/en/3.1/ref/settings/
"""

import os

import dj_database_url
import environ
from corsheaders.defaults import default_headers

env = environ.Env()

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# False if not in os.environ
DEBUG = env("DEBUG", default=False)

# set secret key in production always
SECRET_KEY = env("SECRET_KEY", default="default_secret_key")
LOG_PATH = env("LOG_PATH", default=os.path.join(os.getcwd(), "log"))

HOSTNAME = env("HOSTNAME", default="127.0.0.1")
EXPORT_TOOL_API_URL = env(
    "EXPORT_TOOL_API_URL",
    default="	https://api-prod.raw-data.hotosm.org/v1",
)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", HOSTNAME]
CORS_ALLOW_HEADERS = list(default_headers) + [
    "access-token",
]
if env("GDAL_LIBRARY_PATH", default=False):
    GDAL_LIBRARY_PATH = env("GDAL_LIBRARY_PATH")

OSM_CLIENT_ID = env("OSM_CLIENT_ID")
OSM_CLIENT_SECRET = env("OSM_CLIENT_SECRET")
OSM_URL = env("OSM_URL", default="https://www.openstreetmap.org")
OSM_SCOPE = env("OSM_SCOPE", default="read_prefs")
OSM_LOGIN_REDIRECT_URI = env(
    "OSM_LOGIN_REDIRECT_URI", default="http://127.0.0.1:8000/api/v1/auth/callback/"
)
OSM_SECRET_KEY = env("OSM_SECRET_KEY")


# Limiter
EPOCHS_LIMIT = env("EPOCHS_LIMIT", default=30)
BATCH_SIZE_LIMIT = env("BATCH_SIZE_LIMIT", default=8)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "django.contrib.gis",
    "leaflet",
    "rest_framework",
    "rest_framework_gis",
    "django_filters",
    "corsheaders",
    "login",
    "drf_yasg",
    "celery",
    "django_celery_results",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default="http://127.0.0.1:8000").split(
    ","
)

CORS_ORIGIN_WHITELIST = ALLOWED_ORIGINS

# CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "login.authentication.OsmAuthentication",
    ],
}

ROOT_URLCONF = "aiproject.urls"

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
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]

WSGI_APPLICATION = "aiproject.wsgi.application"


# Database
# https://docs.aiproject.com/en/3.1/ref/settings/#databases


DATABASES = {}

DATABASES["default"] = dj_database_url.config(
    default="postgis://admin:password@localhost:5432/ai", conn_max_age=500
)

# Password validation
# https://docs.aiproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.aiproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.aiproject.com/en/3.1/howto/static-files/

STATIC_URL = "/api_static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "api_static")

if DEBUG:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# celery configuration

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/0"
)  # if you don't want to use redis pass 'django-db' to use app db itself


AUTH_USER_MODEL = "login.OsmUser"

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "OSM": {"type": "apiKey", "name": "access-token", "in": "header"},
    }
}
# get ramp home and set it to environ
RAMP_HOME = env("RAMP_HOME")
os.environ["RAMP_HOME"] = RAMP_HOME

# training workspace
TRAINING_WORKSPACE = env(
    "TRAINING_WORKSPACE", default=os.path.join(os.getcwd(), "training")
)
