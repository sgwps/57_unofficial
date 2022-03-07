from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Subject(models.Model):
    Name = models.CharField(max_length=30)


class MediaPost(models.Model):
    Name = models.CharField(max_length=30)


class Specialization(models.Model):
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=1000)


class Grade(models.Model):
    GraduationYear = models.IntegerField()
    Specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT(), related_name='Class')
    Letter = models.CharField(max_length=1)


class Profile(models.Model):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female'),
        ('n', 'neutral')
    )
    is_teacher = models.BooleanField()
    is_student = models.BooleanField()
    is_manager = models.BooleanField()
    is_mediaStaff = models.BooleanField()
    UserID = models.OneToOneField(User, on_delete=models.CASCADE)
    Gender = models.CharField(max_length=1, choices=GENDERS)
    isConfirmed = models.BooleanField()
    BIO = models.CharField()
    Birthday = models.DateField(blank=True)
    city = models.IntegerField()

    @classmethod
    def create(cls, attrs):
        '''''''
        if attrs.is_teacher:

        if attrs.is_student:

@receiver(post_save, sender)
def save_user_


# Magic from Habr section link for original topic: https://habr.com/ru/post/313764/
# разбить на классы по Positions???


@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_(sender, instance, **kwargs):
    instance.profile.save()


class Teacher(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    Subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT(), related_name='Subject')  #many to many - remake
    working_currently = models.BooleanField()


class Student(models.Model):
    ProfileID = models.OnesaveoOneField(Profile, on_delete=models.CASCADE)
    Grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT(), related_name='Class')


class Manager(models.Model):
    post = models.CharField(max_length=50)
    working_currently = models.BooleanField()


class MediaStaff(models.Model):
    post = models.CharField(max_length=50)







