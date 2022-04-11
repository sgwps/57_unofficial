from django.db import models


class NewsTest(models.Model):
    link_to_preview = models.CharField(max_length=200)
    card_title = models.CharField(max_length=60)
    card_description = models.CharField(max_length=150)
    last_updated = models.CharField(max_length=30)
