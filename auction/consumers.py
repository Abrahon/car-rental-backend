# auctions/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'

        # Join auction group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive bid from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        bid_amount = data['bid_amount']
        user_id = self.scope['user'].id

        # Here, you can validate the bid, update DB, etc.

        # Send bid update to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'auction_update',
                'bid_amount': bid_amount,
                'user_id': user_id
            }
        )

    # Receive message from group
    async def auction_update(self, event):
        await self.send(text_data=json.dumps({
            'bid_amount': event['bid_amount'],
            'user_id': event['user_id']
        }))
