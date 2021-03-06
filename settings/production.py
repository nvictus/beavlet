from settings import *
import dj_database_url

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = env_var('DJ_DEBUG', False)
TEMPLATE_DEBUG = DEBUG

# dj_database_url lets django use the DATABASE_URL environment variable 
# to configure the database
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///:memory:')
}

if not DEBUG:
    ALLOWED_HOSTS = [env_var('HOSTNAME', 'beavlet-nbviewer.herokuapp.com')]

    if env_var('USE_AWS', False):
        STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
        AWS_STORAGE_BUCKET_NAME = env_var('AWS_STORAGE_BUCKET_NAME')
        AWS_ACCESS_KEY_ID       = env_var('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY   = env_var('AWS_SECRET_ACCESS_KEY')
        #AWS_PRELOAD_METADATA = True # necessary to fix manage.py collectstatic command to only upload changed files instead of all files
        S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
        STATIC_URL = S3_URL