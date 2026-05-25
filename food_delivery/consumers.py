import json

from channels.generic.websocket import AsyncWebsocketConsumer


# =====================================================
# LIVE ORDER TRACKING CONSUMER
# =====================================================

class OrderTrackingConsumer(

    AsyncWebsocketConsumer

):

    async def connect(self):

        self.order_id = self.scope['url_route']['kwargs']['order_id']

        self.room_group_name = (

            f'order_{self.order_id}'

        )

        # JOIN ROOM

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )

        await self.accept()

        # SEND CONNECTION MESSAGE

        await self.send(

            text_data=json.dumps({

                'type': 'connection',

                'message': 'Connected to live order tracking',

                'order_id': self.order_id,

            })

        )

    # =================================================
    # DISCONNECT
    # =================================================

    async def disconnect(

        self,
        close_code

    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name

        )

    # =================================================
    # RECEIVE MESSAGE
    # =================================================

    async def receive(

        self,
        text_data

    ):

        data = json.loads(text_data)

        status = data.get('status')

        latitude = data.get('latitude')

        longitude = data.get('longitude')

        eta = data.get('eta')

        # BROADCAST TO ROOM

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                'type': 'send_tracking_update',

                'status': status,

                'latitude': latitude,

                'longitude': longitude,

                'eta': eta,

            }

        )

    # =================================================
    # SEND TRACKING UPDATE
    # =================================================

    async def send_tracking_update(

        self,
        event

    ):

        await self.send(

            text_data=json.dumps({

                'type': 'tracking_update',

                'status': event['status'],

                'latitude': event['latitude'],

                'longitude': event['longitude'],

                'eta': event['eta'],

            })

        )


# =====================================================
# GROUP ORDER CONSUMER
# =====================================================

class GroupOrderConsumer(

    AsyncWebsocketConsumer

):

    async def connect(self):

        self.group_code = self.scope['url_route']['kwargs']['group_code']

        self.room_group_name = (

            f'group_order_{self.group_code}'

        )

        # JOIN GROUP ROOM

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )

        await self.accept()

        # CONNECTION MESSAGE

        await self.send(

            text_data=json.dumps({

                'type': 'connection',

                'message': 'Connected to group order room',

                'group_code': self.group_code,

            })

        )

    # =================================================
    # DISCONNECT
    # =================================================

    async def disconnect(

        self,
        close_code

    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name

        )

    # =================================================
    # RECEIVE GROUP MESSAGE
    # =================================================

    async def receive(

        self,
        text_data

    ):

        data = json.loads(text_data)

        action = data.get('action')

        user = data.get('user')

        item = data.get('item')

        quantity = data.get('quantity')

        total_amount = data.get('total_amount')

        # BROADCAST GROUP UPDATE

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                'type': 'send_group_update',

                'action': action,

                'user': user,

                'item': item,

                'quantity': quantity,

                'total_amount': total_amount,

            }

        )

    # =================================================
    # SEND GROUP UPDATE
    # =================================================

    async def send_group_update(

        self,
        event

    ):

        await self.send(

            text_data=json.dumps({

                'type': 'group_update',

                'action': event['action'],

                'user': event['user'],

                'item': event['item'],

                'quantity': event['quantity'],

                'total_amount': event['total_amount'],

            })

        )