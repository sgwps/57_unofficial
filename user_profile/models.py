from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Subject(models.Model):
    Name = models.CharField(max_length=40)


class MediaPost(models.Model):
    Name = models.CharField(max_length=30)


class Specialization(models.Model):
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=1000)


class Grade(models.Model):
    GraduationYear = models.IntegerField()
    Specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='Class')
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
    User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    Gender = models.CharField(max_length=1, choices=GENDERS)
    isConfirmed = models.BooleanField()
    BIO = models.CharField(blank=True, max_length=500)
    Birthday = models.DateField(blank=True)
    city = models.IntegerField(blank=True)


    @staticmethod
    def create(data):  #data - json or dict??
        email = data["email"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data.get("username", "")
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        user.save()
        profile = Profile
        profile.User = user
        profile.Gender = data.get("gender", "n")
        profile.is_teacher = data.get("is_teacher", False)
        profile.is_student = data.get("is_student", False)
        profile.Birthday = data.get("bday", None)
        profile.save()
        if profile.is_student:
            Student.create(data.get("student", dict()), profile)
        if profile.is_teacher:
            Teacher.create(data.get("teacher", dict()), profile)


@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

'''
    @classmethod
    def create(cls, attrs):
        '''''''
        if attrs.is_teacher:

        if attrs.is_student:

@receiver(post_save, sender)
def save_user_


# Magic from Habr section link for original topic: https://habr.com/ru/post/313764/
# разбить на классы по Positions???



'''
class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile")
    Subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='Subject', blank=True)  #many to many - remake
    working_currently = models.BooleanField()


    @staticmethod
    def create(data, profile):
        teacher = Teacher
        teacher.profile = profile


class Student(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    Grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='Class', blank=True)


class Manager(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50, blank=True)
    working_currently = models.BooleanField()


class MediaStaff(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50)


@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

