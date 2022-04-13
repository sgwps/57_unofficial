from django.db import models
from django_quill.fields import QuillField
# Create your models here.

class Article(models.Model):
    content = QuillField()
    date_created = models.DateTimeField(blank=True, null = True)
    editor = models.IntegerField(blank=True, null = True)
    time_flag = models.DateTimeField(blank=True, null=True)