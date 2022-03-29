
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# pip install channels

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))

    def disconnect(self, code):
        print("stop")