from django.urls import re_path

from . import consumers


websocket_urlpatterns = [

    # =================================================
    # LIVE ORDER TRACKING
    # =================================================

    re_path(

        r'ws/order/(?P<order_id>\w+)/$',

        consumers.OrderTrackingConsumer.as_asgi()

    ),

    # =================================================
    # GROUP ORDER LIVE ROOM
    # =================================================

    re_path(

        r'ws/group-order/(?P<group_code>\w+)/$',

        consumers.GroupOrderConsumer.as_asgi()

    ),

]