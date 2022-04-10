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

def GetAllInDict(Model):
    result = GetAll(Model)
    result_dict = dict()
    for i in result:
        result_dict[i[0]] = i[1]
    return result_dict

class Specialization(models.Model):
    name = models.CharField(max_length=40, null=True)


class Subject(models.Model):
    name = models.CharField(max_length=40, null=True)


class MediaPost(models.Model):
    name = models.CharField(max_length=40, null=True)

class Gender(models.Model):  # ISO 5218
    name = models.CharField(max_length=20, null=True)


class Grade(models.Model):
    graduation_year = models.IntegerField()
    specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='grades', null=True)
    letter = models.CharField(max_length=1, null=True, blank='True')

    @staticmethod
    def GetGradesByYear(year):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н' ,'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
        result = list()
        grades_list = Grade.objects.filter(graduation_year=year)
        for grade in grades_list:
            spec = grade.specialization
            if spec != None:
                spec = spec.name
            result.append((grade.id, (grade.letter, spec)))
            if grade.letter != None:
                letters.remove(grade.letter)
        res_dict = {
            "grades":result,
            "letters":letters
        }
        return res_dict

    @staticmethod
    def GetGrade(data):
        if data['grade_year'] == None:
            return None
        if data['grade_letter'] != 'other':
            return Grade.objects.get_or_create(graduation_year=data['graduation_year'], letter=data.get('grade_letter'))
        else:
            grade = Grade()
            grade.graduation_year = data['graduation_year']
            if data.get('grade', {}).get('custom_grade_letter') != None:
                grade.letter = data.get('grade', {}).get('custom_grade_letter')
                grade.specialization = Specialization.objects.get(name=data['grade']['specialization'])
            grade.save()
            return grade




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
    city = models.IntegerField(blank=True, null=True)


    @staticmethod
    def create(data):  #data - json or dict??
        print(data)
        user = create_user(data['user'])
        user.save()
        profile = Profile()
        profile.user = user
        print(data["profile"].get("gender"))
        profile.gender = Gender.objects.get(pk=data["profile"].get("gender"))
        birthday = data["profile"].get("birthday")
        if birthday != None:
            profile.birthday = birthday
        profile.save()
        if data.get('is_student') == True:
            profile.is_student = True
            Student.create(data['student'], profile)
        profile.save()


class Teacher(models.Model):
    subjects = models.ManyToManyField(Subject)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')

    @staticmethod
    def create(data, profile):
        teacher = Teacher()
        teacher.profile = profile
        subjects = data.get("subjects", tuple())
        for subject_id in subjects:
            teacher.subjects.add(Subject.objects.get(pk=subject_id))
        other = data.get("other_subjects", tuple())
        for subject_name in other:
            subject = Subject.objects.create(name=subject_name)
            teacher.subjects.add(subject)
        teacher.save()


class Student(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='students', blank=True, null=True)


    @staticmethod
    def create(data, profile):
        student = Student()
        student.profile = profile
        if data.get('graduation_year') != None:
            grade = Grade.GetGrade(data)
        student.save()



class Manager(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50, blank=True)
    working_currently = models.BooleanField()


class MediaStaff(models.Model):
    ProfileID = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.CharField(max_length=50)


