"""
WSGI config for beavlet project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
# Set the appropriate settings module.
import os
from settings import env_var

env = env_var('ENVIRONMENT')
if env == 'STAGING':
    mode = 'staging'
elif env == 'PRODUCTION':
    mode = 'production'
else:
    mode = 'development'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.{}".format(mode))

# Create the application object.
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
if not env_var('USE_AWS', False):
    from dj_static import Cling
    application = Cling(application)