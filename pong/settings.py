# /pong/settings.py

"""
Django settings for pong project.

Generated by 'django-admin startproject' using Django 3.2.
"""

import os
import logging.config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345678'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels', 
    'pong.game',
    #'django_db_conn_pool',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pong', 'static')],  # Ensure templates are found
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

ASGI_APPLICATION = 'pong.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': None,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pong/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Channels
# Define the channel layers for WebSockets
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

'''LOGGING = {
    'version': 1,  # Django requires this key
    'disable_existing_loggers': False,  # Keep Django's default loggers
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',  # Allows to use Python's new style string formatting
        },
    },
    'handlers': {
        'console': {  # Log to the console
            'level': 'DEBUG',  # Minimum level of messages that should be handled
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # Use the simple formatter defined above
        },
    },
    'loggers': {
        'django': {  # The main logger for Django itself
            'handlers': ['console'],
            'level': 'DEBUG',  # Minimum log level to be logged
            'propagate': False,  # Prevents log propagation to other loggers
        },
    },
}'''

"""
LOGGING = {
    'version': 1,  # The version of the logging configuration schema
    'disable_existing_loggers': False,  # Allows existing loggers to keep logging
    'formatters': {  # Defines how log messages will be formatted
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Formatter that outputs logs in JSON format, which is ideal for ingestion by Logstash.
        },
        'default': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            # This is a basic text formatter with timestamp, log level, logger name, line number, and the actual message.
        },
    },
    'handlers': {  # Handlers determine where the log messages are sent
        'file': {
            'level': 'INFO',  # Minimum log level to be handled (INFO and above)
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),  # The file where logs will be saved
            'formatter': 'json',  # Uses the JSON formatter defined above
        },
        'console': {
            'level': 'DEBUG',  # Minimum log level to be handled (DEBUG and above)
            'class': 'logging.StreamHandler',
            'formatter': 'default',  # Uses the default text formatter
        },
    },
    'loggers': {  # Loggers are the actual log streams that get configured
        'django': {  # The Django logger catches all messages sent by the Django framework
            'handlers': ['file', 'console'],  # Sends logs to both the file and the console
            'level': 'DEBUG',  # Minimum log level to be logged
            'propagate': True,  # If True, messages will be passed to the parent loggers as well
        },
    },
}
"""
