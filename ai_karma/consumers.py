import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AIKarmaConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.channel_layer.group_add(
            "ai_karma_alerts",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            "ai_karma_alerts",
            self.channel_name
        )

    async def send_alert(self, event):

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'risk_level': event['risk_level']
        }))