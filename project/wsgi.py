"""
WSGI config for portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from os.path import abspath, dirname
from sys import path

from django.core.wsgi import get_wsgi_application

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.base")

application = get_wsgi_application()
