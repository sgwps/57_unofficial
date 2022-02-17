from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    email = models.EmailField('Email', unique = True)
    user_name = models.CharField('Username', max_length = 150, unique = True)
    first_name = models.CharField('First name', max_length = 150, unique = True)
    second_name = models.CharField('Second name',max_length = 150, unique = True)

    def __str__(self):
        return self.user_name

class ProfileApp(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.CharField()
    

        