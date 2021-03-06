# Django settings for quickstart project.
import os
import sys
from secret_settings import *
# Django settings for mysite project.

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ADMIN_APP = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         "../administrator"))
#define your own rule to check whether dev or production
if 'devasia' in os.getcwd():
    LOCALHOST = True
    DEBUG = True
else:
    LOCALHOST = False
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Determine if we are running in the test environment.
TEST = False
manage_command = filter(lambda x: x.find('manage.py') != -1, sys.argv)
if len(manage_command) != 0:
    command = sys.argv.index(manage_command[0]) + 1
    if command < len(sys.argv):
        TEST = sys.argv[command] == "test"


DEBUG = True
TEMPLATE_DEBUG = DEBUG

#SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fratography',
        'USER': 'fratography',
        'PASSWORD': 'fratography',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'fratography_static')
UPLOAD_PATH = MEDIA_ROOT + "/uploads/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://198.58.96.200/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0&amp;t%=o9ki$gw00)a#s#9$_0f9-18kxn8l4t+els)di$*q(_py='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'app.context_processors.upload_path',
    'app.context_processors.categories'
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mysite.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(ADMIN_APP, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'administrator',
    'calendarapp',
    'south'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# JSON status codes to communicate with the front end
APP_CODE = {
    "ACCESS DENIED": "access_denied",
    "INVALID REQUEST": "invalid_request",
    "FORM ERROR": "form_error",
    "SYSTEM ERROR": "system_error",
    "CALLBACK": "callback",
    "SERVER MESSAGE": 'server_message',
    "PAGE LOADED": 'page_loaded',
    "REGISTERED": 'registered',
    "LOGIN": 'login',
    "SAVED": "saved",
    "DELETED": "deleted",
    "UPDATED": "updated",
    "REDIRECT": "redirect"
}

PRICE_TYPE = {"PRICE_PER_HOUR": "price_per_hour"}

APP_USERNAME = "dev"
APP_PASSWORD = "password"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
ADMIN_EMAIL ="mgoodwin1@gmail.com"
SITE_URL = "http://198.58.96.200/"
AUTH_PROFILE_MODULE = 'app.UserProfile'

if LOCALHOST:
    SITE_URL = "http://localhost:8000"
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fratography',
        'USER': 'retailer',
        'PASSWORD': 'retailer',
        'HOST': '',
        'PORT': ''
        }
    }
    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'administrator',
    'calendarapp',
    'south',
    'django_extensions'

    # Uncomment the next line to enable the admin:
        # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
    )
    MEDIA_URL = 'http://localhost:8090/fratography_static/'
    FBAPP_ID = ""
    FBAPP_SECRET = ""
    FBAPP_REDIRECT_URI = "http://localhost:8000/fbauth"
    TWITTER_KEY = 'local key'
    TWITTER_SECRET = 'local secret'
    GOOGLE_SECRET = "local secret"
    GOOGLE_CLIENT_ID = "local id"
    GOOGLE_REDIRECT_URI = "https://localhost/oauth2callback"
