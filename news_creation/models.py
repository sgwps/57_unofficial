from django.db import models
from django_quill.fields import QuillField
# Create your models here.

class Article(models.Model):
    content = QuillField()
    date_created = models.DateTimeField(blank=True)
    date_uploaded = models.DateTimeField(blank=True)
    if_uploaded = models.BooleanField(blank=True)
