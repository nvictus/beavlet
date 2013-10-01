import os
import dj_database_url

from beavlet.settings.common import *

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['beavlet-nbviewer.herokuapp.com']

if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgres://localhost'
    #'postgres://tinhnyxptawfee:v-A44763l5OSarDWweeXO0qtf6@ec2-54-225-123-71.compute-1.amazonaws.com:5432/d8587t6n8fkump'

DATABASES = {
    'default': dj_database_url.config()
}