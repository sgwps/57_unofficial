from django.db import models
from django.urls import clear_script_prefix
from user_profile import models as user_models

class Publication(models.Model):
    content = models.FileField()
    is_article = models.BooleanField(editable=False)
    date_created = models.DateTimeField()

'''
def ParentDeletion():
    raise NotImplementedError


class Comment(models.Model):
    self_publication_id = models.ForeignKey(to=Publication, on_delete=models.CASCADE, related_name="comments")
    parent_id = models.ForeignKey(to=Publication, on_delete=ParentDeletion, related_name="comments")
    user_id = models.ForeignKey(to=user_models.User, on_delete=models.SET_NULL(), related_name="comments", blank=True, null=True)

'''
#  check set null    



