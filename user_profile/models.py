from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
'''
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


'''

class OurUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.IntegerField()
    userName = models.CharField(max_length=100)
    Email = models.EmailField()
    ifConfirmed = models.BooleanField()
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    BIO = models.CharField(max_length=250)
    birthday = models.DateField()
    position = models.ForeignKey(to=Position, on_delete=models.SET_NULL(), related_name='Position')
    subject = models.ForeignKey(to=Subject, on_delete=models.SET_NULL(), related_name='Subject')
    Class = models.ForeignKey(to=Class, on_delete=models.SET_NULL(), related_name='Class')
    mediaPost = models.IntegerField()
    city = models.IntegerField()

# Magic from Habr section

@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        OurUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_(sender, instance, **kwargs):
    instance.profile.save()






class Position(models.Model):
    ID = models.IntegerField()
    Title = models.CharField(max_length=30)


class Subject(models.Model):
    ID = models.IntegerField()
    Name = models.CharField(max_length=30)


class Classes(models.Model):
    ID = models.IntegerField()
    GraduationYear = models.DateField()
    Profile =  models.ForeignKey(to=Class, on_delete=models.SET_NULL(), related_name='Specializations')
    Letter = models.CharField(max_length=5)


class Spec(models.Model):
    # Specialization
    ID = models.IntegerField()
    Name = models.CharField(max_length=30)





