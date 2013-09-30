import dj_database_url

from beavlet.settings.common import *

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config()
}
