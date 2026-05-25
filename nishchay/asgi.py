"""
ASGI config for nishchay project.
"""

import os

from channels.routing import (

    ProtocolTypeRouter,
    URLRouter,

)

from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application


# =====================================================
# DJANGO SETTINGS
# =====================================================

os.environ.setdefault(

    'DJANGO_SETTINGS_MODULE',

    'nishchay.settings'

)


# =====================================================
# DJANGO ASGI APP
# =====================================================

django_asgi_app = get_asgi_application()


# =====================================================
# WEBSOCKET ROUTINGS
# =====================================================

import accounts.routing

import ai_karma.routing

import food_delivery.routing


# =====================================================
# MAIN APPLICATION
# =====================================================

application = ProtocolTypeRouter({

    # =================================================
    # HTTP
    # =================================================

    "http": django_asgi_app,

    # =================================================
    # WEBSOCKET
    # =================================================

    "websocket": AuthMiddlewareStack(

        URLRouter(

            accounts.routing.websocket_urlpatterns +

            ai_karma.routing.websocket_urlpatterns +

            food_delivery.routing.websocket_urlpatterns

        )

    ),

})