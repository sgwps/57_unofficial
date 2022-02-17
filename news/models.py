from tkinter.tix import Tree
from django.db import models

# Create your models here.
class NewsApp(models.Model):
    news = models.CharField(max_length = 200)

class Post(models.Model):
    newsapp = models.ForeignKey(NewsApp, on_delete = models.CASCADE)
    paragraph = models.TextField(blank = True, null = True)

    

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    image = models.ImageField(null = True, blank = True, upload_to = "images/")
    
    