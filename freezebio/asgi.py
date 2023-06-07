"""
ASGI config for freezebio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


import os,django
from channels.auth import AuthMiddlewareStack
from .consumers import MyMqttConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .routing import websockets_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freezebio.settings')
django.setup()
application = get_asgi_application()

application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'mqtt': MyMqttConsumer.as_asgi(),
        'websocket':URLRouter(websockets_url),
    })

# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         await django_application(scope, receive, send)
#     elif scope['type'] == 'websocket':
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
