from django.db import models

# Create your models here.

from django.db import models
from django.urls import clear_script_prefix
from user_profile import models as user_models

class Article(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField()




class Comment(models.Model):
    artcile = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name="comments")
    parent_id = models.ForeignKey(to='self', on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    user_id = models.ForeignKey(to=user_models.User, on_delete=models.SET_NULL(), related_name="comments", blank=True, null=True)
    content = models.TextField()
    date_created = models.DateTimeField()
