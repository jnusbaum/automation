"""
Django settings for automation project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&xew$54tr%+yo^%smili0gix!rehhi_u-$46^8k80wwy#azt9n'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'devices.apps.DevicesConfig',
    'devices_views.apps.DevicesViewsConfig',
    'heating.apps.HeatingConfig',
    'heating_views.apps.HeatingViewsConfig',
    'hotwater.apps.HotwaterConfig',
    'hotwater_views.apps.HotwaterViewsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'automation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'automation/templates'),
                 os.path.join(BASE_DIR, 'heating_views/templates'),
                 os.path.join(BASE_DIR, 'hotwater_views/templates'),
                 os.path.join(BASE_DIR, 'devices_views/templates')]
        ,
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

WSGI_APPLICATION = 'automation.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'automation',
        'USER': 'automation',
        'PASSWORD': 'zaxxon',
        'HOST': '192.168.0.134',
        # 'HOST': 'automation.c0bnlhkxko2m.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'tempcapture': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/rjn/Projects/automation/log/tempcapture.log',
            # 'filename': '/home/ubuntu/automation/log/tempcapture.log',
        },
        'relaycapture': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 'filename': '/home/ubuntu/automation/log/relaycapture.log',
            'filename': '/home/rjn/Projects/automation/log/relaycapture.log',
        },
        'devstatuscapture': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 'filename': '/home/ubuntu/automation/log/devstatuscapture.log',
            'filename': '/home/rjn/Projects/automation/log/devstatuscapture.log',
        },
        'deviceconfig': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 'filename': '/home/ubuntu/automation/log/deviceconfig.log',
            'filename': '/home/rjn/Projects/automation/log/deviceconfig.log',
        },
    },
    'loggers': {
        'tempcapture': {
            'handlers': ['tempcapture'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'relaycapture': {
            'handlers': ['relaycapture'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'devstatuscapture': {
            'handlers': ['devstatuscapture'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'deviceconfig': {
            'handlers': ['deviceconfig'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/automation/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# app specific settings - should they be here?

# DATASERVER_HOST = 'http://ec2-18-191-56-78.us-east-2.compute.amazonaws.com/automation'
MQTTHOST = 'localhost'
# TEMPMQTTID = 'tempcapture'
RELAYMQTTID = 'relaycapture'
DEVCFGMQTTID = 'deviceconfig'
DEVSTATUSMQTTID = 'devstatuscapture'
BASETOPIC = 'sorrelhills'

DATASERVER_HOST = 'http://127.0.0.1:8000/automation'
MQTTHOST = '192.168.0.134'
# TEMPMQTTID = 'testtempcapture'
# RELAYMQTTID = 'testrelaycapture'
# DEVCFGMQTTID = 'testdeviceconfig'
# DEVSTATUSMQTTID = 'testdevstatuscapture'
# BASETOPIC = 'sorrelhills'
