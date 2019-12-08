from __future__ import absolute_import

import ast
import os

import dj_database_url
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'cj36%5xda7q5+ov)wz+(=vt7d81ka^xx!5%0)nx=z2i&)*5r^',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split()

GRAPPELLI_ADMIN_TITLE = 'FOOT TRIAL'

# Application definition.

DJANGO_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'django_slack',
    'rest_framework',
    'rest_framework.authtoken',
]

LOCAL_APPS = [
    'apps.customuser',
    'apps.home',
    'apps.hospital',
    'apps.patient',
    'apps.message',
    'apps.publicip',
    'foottrial',
]

if not DEBUG:
    THIRD_APPS += [
        'opbeat.contrib.django',
    ]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

# REST framework API configuration.
REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'PAGINATE_BY': 30,
    'MAX_PAGINATE_BY': 100,
}

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

if not DEBUG:
    MIDDLEWARE_CLASSES += [
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    ]

ROOT_URLCONF = 'foottrial.urls'

# Templates.

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

WSGI_APPLICATION = 'foottrial.wsgi.application'


# Database.

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'OPTIONS': {
                'timeout': 20,
            }
        },
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get(
                'DB_URL',
                'postgres://oscar:oscar@localhost:5432/foottrial',
            ),
        ),
    }

# Internationalization.
LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SLACK
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', '')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '')
SLACK_USERNAME = os.environ.get('SLACK_USERNAME', '')

# Static files (CSS, JavaScript, Images).
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles')
)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Media files.
MEDIA_URL = '/media/'

MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

# Custom User Model.

AUTH_USER_MODEL = 'customuser.MyUser'

AUTHENTICATION_BACKENDS = (
    'apps.customuser.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Celery and RabbitMQ.

BROKER_URL = os.getenv('BROKER_URL')

CELERY_TIMEZONE = TIME_ZONE

# Scheduler.

SCHEDULER_HOUR = int(os.getenv('SCHEDULER_HOUR', 8))
SCHEDULER_MINUTE = int(os.getenv('SCHEDULER_MINUTE', 0))

CELERYBEAT_SCHEDULE = {
    'send-messages-every-day': {
        'task': 'foottrial.tasks.send_scheduled_messages',
        'schedule': crontab(
            hour=SCHEDULER_HOUR,
            minute=SCHEDULER_MINUTE,
        ),
    },
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_IGNORE_RESULT = False

# opbeat
OPBEAT = {
    'ORGANIZATION_ID': os.environ.get('OPBEAT_ORGANIZATION_ID', ''),
    'APP_ID': os.environ.get('OPBEAT_APP_ID', ''),
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN', ''),
    'DEBUG': False,
}


QUEUE_NAME = os.environ.get('QUEUE_NAME', 'message')
QUEUE_EXCHANGE = os.environ.get('QUEUE_EXCHANGE', 'messages_exchange')
QUEUE_KEY = os.environ.get('QUEUE_KEY', 'messages_key')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'foottrial': {
            'level': 'WARNING',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        # Log errors from the Opbeat module to the console (recommended)
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
