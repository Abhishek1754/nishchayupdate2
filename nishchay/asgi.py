"""
ASGI config for nishchay project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# 🚀 ROUTINGS
import accounts.routing
import ai_karma.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nishchay.settings')

# 🚀 DJANGO APP
django_asgi_app = get_asgi_application()

# 🚀 MAIN APPLICATION
application = ProtocolTypeRouter({

    # HTTP
    "http": django_asgi_app,

    # WEBSOCKET
    "websocket": AuthMiddlewareStack(
        URLRouter(

            # 🔥 ALL WEBSOCKET ROUTES
            accounts.routing.websocket_urlpatterns +
            ai_karma.routing.websocket_urlpatterns

        )
    ),
})