"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# setup log file
with open('request_logs.txt', 'r+') as file:
    pass


# ============================> LOAD ENV VARS <============================
# load .env file from base dir
load_dotenv(str(BASE_DIR) + r'\.env')
ENV_PRODUCTION = os.environ.get("PRODUCTION", '0')
ENV_TZ = os.environ.get("TZ", '')

ENV_EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", '')
ENV_EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", '')

ENV_USE_DATABASE = os.environ.get("USE_DATABASE", 'remote')
ENV_DATABASE_CONN_URL = os.environ.get("DATABASE_CONN_URL", '')
ENV_HEROKU_POSTGRESQL_ROSE_URL = os.environ.get("HEROKU_POSTGRESQL_ROSE_URL", '') # need to be updated manually in local

ENV_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", '')
ENV_GITHUB_PRIVATE_REPO = os.environ.get("GITHUB_PRIVATE_REPO", '')
ENV_GITHUB_LETTER_PATH = os.environ.get("GITHUB_LETTER_PATH", '')
ENV_GITHUB_LETTER_INTRO_PATH = os.environ.get("GITHUB_LETTER_INTRO_PATH", '')

ENV_DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", '')
ENV_API_KEY = os.environ.get("API_KEY", '')

# environment check
def is_production():
    if ENV_PRODUCTION == '0':
        return False
    else:
        return True

# ============================> SECURITY <============================
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_DJANGO_SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
# false caused error 500 when running the server 'locally'
# this happen because additional variable settings at bottom line
if is_production():
    DEBUG = False
else:
    DEBUG = True
print(f"debug: {is_production()}")
ALLOWED_HOSTS = ['*']


# ============================> APPLICATION DEFINITION <============================
INSTALLED_APPS = [
    'root_app',
    'api_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middleware.RequestMonitor',
]
ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# ============================> DATABASE <============================
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if ENV_USE_DATABASE == 'local':
    print("database type: local")
    # local database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'science2masu-db.sqlite3',
        }
    }
else:
    print("database type: remote")
    # remote database
    DATABASES = {
        'default': dj_database_url.config(default=ENV_HEROKU_POSTGRESQL_ROSE_URL)
    }
#from django.db import connection
#print(connection.settings_dict['NAME'])

# ============================> PASSWORD VALIDATION <============================
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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


# ============================> INTERNATIONALIZATION <============================
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = ENV_TZ


# ============================> STATIC FILES (css, javascript, images) <============================
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [(BASE_DIR / 'static')] # Extra places for django to find static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================> DEFAULT PRIMARY KEY FIELD TYPE <============================
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================> EMAIL CONFIG <============================
# https://docs.djangoproject.com/en/4.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ENV_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ENV_EMAIL_HOST_PASSWORD


# ============================> SESSION CONFIG <============================
# https://docs.djangoproject.com/en/4.0/ref/settings/#sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600

# ============================> CSRF <============================
# https://docs.djangoproject.com/en/4.0/ref/csrf/
CSRF_TRUSTED_ORIGINS = ['https://science2masu.herokuapp.com', 'https://science2masu.up.railway.app', 'http://127.0.0.1']