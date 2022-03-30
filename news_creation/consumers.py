
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from news_creation.models import Article


# pip install channels

class Editor(WebsocketConsumer):
    def connect(self):
        self.accept()
    

    def receive(self, text_data=None, bytes_data=None):
        print(self.scope)  # get IP
        #self.id = json.loads(text_data)["id"]
        #article = Article.objects.get(pk=id)
        print("socket: ", text_data)


    def disconnect(self, code):
        print("stop")