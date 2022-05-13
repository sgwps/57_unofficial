from django.db import models
from user_profile.models import  User
# Create your models here.

class Chat(models.Model):
    id = models.IntegerField(blank=True, null=True)
    user_1 = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=true)
    user_2 = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=true)


class Message(models.Model):
    id = models.IntegerField(blank=True, null = True)
    chat_id =  models.ForeignKey(to=Chat,on_delete=models.SET_NULL,null = true)
    sender = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=true)
    content  = models.CharField(max_length=300)
