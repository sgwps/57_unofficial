from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Test(models.Model):
    test2 = models.CharField(max_length=1, default='y')
    test3 = models.CharField(max_length=1, default='y')