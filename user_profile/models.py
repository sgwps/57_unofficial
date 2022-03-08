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
    UserID = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    Gender = models.CharField(max_length=1, choices=GENDERS)
    isConfirmed = models.BooleanField()
    BIO = models.CharField(blank=True, max_length=500)
    Birthday = models.DateField(blank=True)
    city = models.IntegerField(blank=True)
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


@receiver(post_save, sender=User)
def create_user_(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
'''
class Teacher(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile")
    Subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='Subject', blank=True)  #many to many - remake
    working_currently = models.BooleanField()


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


class UserAdapter:
    def __init__(self, id=0):
        self.id = id

    @staticmethod
    def create(self, data):
        try:
            email = data["email"]
            password = data["password"]
            first_name = data["first_name"]
            last_name = data["last_name"]
        except:
            raise NotImplementedError
        username = data.get("username", "")

        user = User(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        user.save()
        profile = User.profile
        gender = data.get("gender", "n")
        is_teacher = data.get("is_teacher", False)
        is_student = data.get("is_student", False)
        birthday = data.get("bday", None)
        profile.Gender = gender
        profile.is_teacher = is_teacher
        profile.is_student = is_student
        profile.Birthday = birthday
        profile.save()
        if is_teacher:
            teacher = Teacher(ProfileID=profile)
            teacher.working_currently = data.get('working_currently', False)
            teacher.save()
        if is_student:
            student = Student(ProfileID=profile)
            student.save()





