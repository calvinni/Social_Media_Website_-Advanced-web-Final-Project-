import json
from .models import Chat, ChatRoom
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        userID = text_data_json['userID']
        roomID = text_data_json['roomID']
        chat = Chat(
            message=message,
            user_id_id=userID,
            room_id_id=roomID
            )
        chat.save()
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'userID': userID,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
