from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField('Email', unique = True)
    user_name = models.CharField('Username', max_length = 150, unique = True)
    first_name = models.CharField('First name', max_length = 150, unique = True)
    second_name = models.CharField('Second name',max_length = 150, unique = True)

class ProfileApp(models.Model):
    user = newsapp = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.CharField()
    

        