"""
WSGI config for setup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

application = get_wsgi_application()

# Create superuser if it does not exist
import sys
from django.conf import settings

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))
import create_instances

if settings.DEBUG == True:
    create_instances.create()
