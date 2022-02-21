from django.db import models


class Article(models.Model):
    headline = models.CharField(max_length=100)
    date_created = models.DateField()
    date_uploaded = models.DateField(blank=True)
    preview_image = models.ImageField(upload_to='preview', blank=True)
    preview_text = models.CharField(blank=True, max_length=300)
    content_empty = models.BooleanField()
    article_content = models.TextField(blank=True)  #json
# authors - many to many (position, news, userid)


