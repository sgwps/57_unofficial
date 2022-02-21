from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Position(models.Model):
    Name = models.CharField(max_length=30)


class Subject(models.Model):
    Name = models.CharField(max_length=30)


class Specialization(models.Model):
    # Specialization
    Name = models.CharField(max_length=30)


class Grade(models.Model):
    GraduationYear = models.IntegerField()
    Specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='Specializations')
    Letter = models.CharField(max_length=1)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('n', 'neutral')
    )
    User_main = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    isConfirmed = models.BooleanField()
    BIO = models.CharField(max_length=570)
    Birthday = models.DateField(blank=True)
    Position = models.ForeignKey(to=Position, on_delete=models.PROTECT, related_name='Position')
    Subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='Subject')
    Class = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='Class')
    mediaPost = models.IntegerField()
    city = models.IntegerField()

# Magic from Habr section link for original topic: https://habr.com/ru/post/313764/


@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_(sender, instance, **kwargs):
    instance.profile.save()

