
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from news_creation.models import Article


# pip install channels

class Editor(WebsocketConsumer):
    def connect(self):
        self.accept()
    

    def receive(self, text_data=None, bytes_data=None):
        client = self.scope['client']  # get IP
        self.id = json.loads(text_data)["id"]
        if self.id != None:
            article = Article.objects.get(pk=self.id)
            article.editor = client
            article.save()
        


    def disconnect(self, code):
        print(self.id)