import os
from os.path import abspath, basename, dirname

def env_var(key, default=None):
    val = os.getenv(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val

#==============================================================================
# Path configuration
#==============================================================================
# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = PROJECT_ROOT

# Site name:
SITE_NAME = 'beavlet'

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
#path.append(PROJECT_ROOT)

ENVIRONMENT = env_var('ENVIRONMENT', 'DEVELOPMENT')

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

PROJECT_NAME = PROJECT_PATH.split('/')[-1]

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

#==============================================================================
# Security
#==============================================================================

# Make this unique, and don't share it with anybody.
SECRET_KEY = env_var('SECRET_KEY', '')

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    # 'django.contrib.admindocs',
    'gunicorn',
    #'account',
)

# My apps
INSTALLED_APPS += (
    #'core'
    'accounts',
    'filters', #custom template filters
    'apps.blog',
    'apps.nbviewer',
    'apps.dropbox',
    'apps.dillinger',
)

#==============================================================================
# Globalization
#==============================================================================

USE_TZ = True
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en-us'

#==============================================================================
# Static and media settings
#==============================================================================

MEDIA_ROOT = ''
MEDIA_URL = ''

# Absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = 'staticfiles'
# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'
# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
 # Additional locations the staticfiles app will traverse if the 
 # FileSystemFinder finder is enabled, e.g. if you use the collectstatic 
 # or findstatic management command
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'static'),
)
# The file storage engine to use when collecting static files with the 
# collectstatic management command.
# AWS storage backend for Django to get static files from CDN
if env_var('USE_AWS', False):
    INSTALLED_APPS += (
        'storages',
    )
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#==============================================================================
# Templates
#==============================================================================

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    #'account.context_processors.account'
)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#==============================================================================
# Middleware
#==============================================================================

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'account.middleware.LocaleMiddleware',
    #'account.middleware.TimezoneMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#==============================================================================
# Auth / security
#==============================================================================

#==============================================================================
# Error reporting
#==============================================================================

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

#==============================================================================
# Logging
#==============================================================================

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

#==============================================================================
# Dropbox API
#==============================================================================

DROPBOX_APP_KEY = env_var('DROPBOX_APP_KEY', '')
DROPBOX_APP_SECRET = env_var('DROPBOX_APP_SECRET', '')