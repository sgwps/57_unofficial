from django.db import models


class Article(models.Model):
    headline = models.CharField(max_length=200)
    date_created = models.DateField()
    date_uploaded = models.DateField(blank=True)
    preview_image = models.ImageField(upload_to='preview', blank=True)
    preview_text = models.CharField(blank=True)
    content_empty = models.BooleanField()
    article_content = models.CharField(blank=True)  #json
# authors - many to many (position, news, userid)


