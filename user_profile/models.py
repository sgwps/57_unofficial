from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


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
    is_manager = models.BooleanField(default=False)
    is_mediaStaff = models.BooleanField(default=False)
    User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    Gender = models.CharField(max_length=1, choices=GENDERS)
    isConfirmed = models.BooleanField(default=False)
    BIO = models.CharField(blank=True, max_length=500)
    Birthday = models.DateField(blank=True, default=0)
    city = models.IntegerField(blank=True, default=0)


    @staticmethod
    def create(data):  #data - json or dict??
        email = data["email"]
        password = data.get("password", "qwerty")
        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data.get("username", "")
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        user.save()
        profile = Profile()
        profile.User = user
        profile.Gender = data.get("gender", "n")
        profile.is_teacher = data.get("is_teacher", False)
        profile.is_student = data.get("is_student", False)
        profile.Birthday = datetime.strptime(data.get("birth_date", None), "%Y-%m-%d")
        profile.save()
        if profile.is_student:
            Student.create(data.get("student", dict()), profile)
        if profile.is_teacher:
            Teacher.create(data.get("teacher", dict()), profile)



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
    #Subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='Subject', blank=True)  #many to many - remake
    #working_currently = models.BooleanField(blank=True)
    Subject = models.CharField(max_length=40)


    @staticmethod
    def create(data, profile):
        teacher = Teacher()
        teacher.profile = profile
        teacher.Subject = data.get("subject", "")
        teacher.save()


class Student(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # Grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='Class', blank=True)
    Graduation_year = models.IntegerField(blank=True, default=None)

    @staticmethod
    def create(data, profile):
        student = Student()
        student.ProfileID = profile
        student.Graduation_year = data.get("end_year", None)
        student.save()



class Manager(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50, blank=True)
    working_currently = models.BooleanField()


class MediaStaff(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50)


