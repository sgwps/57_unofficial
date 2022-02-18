from django.db import models


class Article(models.Model):
    headline = models.CharField(blank=False, max_length=200)
    date_created = models.DateField(blank=False)
    date_uploaded = models.DateField(blank=False)
    preview_image = models.ImageField(upload_to='preview', blank=True)
    preview_text = models.CharField(blank=True)
    article_content = models.CharField()  #json_dir
# authors - many to many (position, news, userid)


