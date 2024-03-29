"""
WSGI config for chat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# application = get_wsgi_application()

import os

from django.core.wsgi import get_wsgi_application
import socketio

from .controllers.socketioController import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)