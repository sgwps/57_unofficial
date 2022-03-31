from django.db import models
from django_quill.fields import QuillField
# Create your models here.

class Article(models.Model):
    content = QuillField()
    date_created = models.DateTimeField()
    editor = models.GenericIPAddressField(blank=True, null = True)