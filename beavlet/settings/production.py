import os
import dj_database_url

from beavlet.settings.common import *

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgres://localhost'
    #'postgres://tinhnyxptawfee:v-A44763l5OSarDWweeXO0qtf6@ec2-54-225-123-71.compute-1.amazonaws.com:5432/d8587t6n8fkump'

DATABASES = {
    'default': dj_database_url.config()
}

if not DEBUG:
    ALLOWED_HOSTS = ['beavlet-nbviewer.herokuapp.com']

    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

    STATIC_URL = S3_URL