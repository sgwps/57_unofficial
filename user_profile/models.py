from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


def GetAll(Model):    #  for Subject, MediaPost, Specialization, Gender
    result = list()
    model_list = Model.objects.all()
    for item in model_list:
        if item.name != None:
            result.append((item.id, item.name))
    return tuple(result)





class Specialization(models.Model):
    name = models.CharField(max_length=30, null=True)


class Grade(models.Model):
    graduation_year = models.IntegerField()
    specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='grades', null=True)
    letter = models.CharField(max_length=1)

    @staticmethod
    def GetGradesByYear(year):
        result = list()
        grades_list = Grade.objects.filter(graduation_year=year)
        for grade in grades_list:
            spec = grade.specialization.name
            result.append((grade.id, (grade.letter, spec)))
        return tuple(result)


class Subject(models.Model):
    name = models.CharField(max_length=40, null=True)


class MediaPost(models.Model):
    name = models.CharField(max_length=40, null=True)


class Gender(models.Model):  # ISO 5218
    name = models.CharField(max_length=20, null=True)


'''
INSERT INTO user_profile_gender (id, gender) VALUES (0, "not known");
INSERT INTO user_profile_gender (id, gender) VALUES (1, "male");
INSERT INTO user_profile_gender (id, gender) VALUES (2, "female");
INSERT INTO user_profile_gender (id, gender) VALUES (9, "not applicable");
'''


def create_user(data):
    email = data["email"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
    user.save()
    return user


class Profile(models.Model):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_media_staff = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    gender = models.ForeignKey(to=Gender, on_delete=models.PROTECT, related_name='users', default=0)
    is_confirmed = models.BooleanField(default=False)
    bio = models.CharField(blank=True, max_length=1000)
    birthday = models.DateField(blank=True, null=True)
    city = models.IntegerField(blank=True)


    @staticmethod
    def create(data):  #data - json or dict??
        user = create_user(data['user'])
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


class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile")
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


