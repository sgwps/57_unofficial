
import json
from time import sleep
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from news_creation.models import Article
from datetime import datetime


# pip install channels

class Editor(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.saving_mode = False
        self.accept()
        
    

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print("-----", text_data)
        id = text_data_json.get("id")
        if id != None:
            self.id = id
            article = Article.objects.get(pk=self.id)
            article.editor = text_data_json.get("user_id")
            article.save()
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':str(id)
            }
            )

        


    def disconnect(self, close_code):
        article = Article.objects.get(pk=self.id)
        article.editor = None
        if close_code == True:
            article.time_flag = datetime.now()
        else:
            article.time_flag = None
            article.save()
        print(self.id)


    def chat_message(self, event):
        message = event['message']
        print("test26 26")
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
        print("test27")