from settings import *

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = env_var('DJ_DEBUG', True)
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.sqlite3',
    }
}

if not DEBUG:
    ALLOWED_HOSTS = ['*']
    
    if env_var('USE_AWS', False):
        STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
        AWS_STORAGE_BUCKET_NAME = env_var('AWS_STORAGE_BUCKET_NAME')
        AWS_ACCESS_KEY_ID = env_var('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = env_var('AWS_SECRET_ACCESS_KEY')
        S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
        STATIC_URL = S3_URL