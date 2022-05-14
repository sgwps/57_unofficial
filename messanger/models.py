from django.db import models
from user_profile.models import  User
# Create your models here.

class Chat(models.Model):
    users = models.ManyToManyField(to=User, on_delete=models.SET_NULL, null=True)  # on_delete
    name = models.CharField(max_length=300, blank=True, null=True)


class Message(models.Model):
    chat_id =  models.ForeignKey(to=Chat,on_delete=models.SET_NULL)
    sender = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    content  = models.CharField(max_length=300)
