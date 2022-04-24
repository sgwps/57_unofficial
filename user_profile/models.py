from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

def getAll(Model) -> dict:    #  for Subject, MediaPost, Specialization, Gender
    result = dict()
    model_list = Model.objects.all()
    for item in model_list:
        if item.name != None:
            result[item.id] = item.name
    return result


class Specialization(models.Model):
    name = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


    @staticmethod
    def getTuple() -> tuple:
        objects = Specialization.objects.all()
        result = list()
        result.append((0, ""))
        for item in objects:
            result.append((item.id, item.name))
        return tuple(result)
        

class Subject(models.Model):
    name = models.CharField(max_length=40, null=True)


class MediaPost(models.Model):
    name = models.CharField(max_length=40, null=True)
    access_to_publish = models.BooleanField()


class Gender(models.Model):  # ISO 5218
    '''
    INSERT INTO user_profile_gender (id, gender) VALUES (0, "not known");
    INSERT INTO user_profile_gender (id, gender) VALUES (1, "male");
    INSERT INTO user_profile_gender (id, gender) VALUES (2, "female");
    INSERT INTO user_profile_gender (id, gender) VALUES (9, "not applicable");
    '''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    graduation_year = models.IntegerField()
    specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='grades', null=True)
    letter = models.CharField(max_length=1, null=True, blank='True')

    


    @staticmethod
    def getGradesByYear(year : int):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н' ,'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
        result = list()
        grades_list = Grade.objects.filter(graduation_year=year)
        for grade in grades_list:
            if grade.letter != None:
                specialization = grade.specialization
                tuple = ((grade.id, grade.letter, str(grade.specialization)))
                letters.remove(grade.letter)
                result.append(tuple)
        res_dict = {
            "grades":result,
            "letters":letters
        }
        return res_dict


    @staticmethod
    def getGrade(data : dict):
        if data.get('graduation_year') == None:
            return None
        elif data.get('letter') == None:
            return grade.objects.get_or_create(graduation_year=data['graduation_year'], letter=None)
        elif data['letter'] != 'other':
            return grade.objects.get(graduation_year=data['graduation_year'], letter=data['grade_letter'])
        elif data.get('custom_grade') == None:
            return grade.objects.get_or_create(graduation_year=data['graduation_year'], letter=None)
        else:
            grade = Grade()
            grade.graduation_year = data['graduation_year']
            grade.letter = data['custom_grade']['letter']
            grade.specialization = Specialization.objects.get(name=data['grade']['specialization'])
            return grade









class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_media_staff = models.BooleanField(default=False)
    gender = models.ForeignKey(to=Gender, on_delete=models.PROTECT, related_name='users', default=3)
    is_confirmed = models.BooleanField(default=False)
    bio = models.CharField(blank=True, max_length=1000)
    birthday = models.DateField(blank=True, null=True)
    city = models.IntegerField(blank=True, null=True)


    @staticmethod
    def create(data : dict):  #data - json or dict??
        user = user()
        user.email = data["email"]
        user.password = data["password"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.username = data["username"]
        user.gender = Gender.objects.get(pk=int(data.get("gender")))
        user.birthday = data.get("birthday")
        user.save
        if data.get('is_student') == True:
            user.is_student = True
            student.create(data.get('student', {}), user)
        if data.get('is_teacher') == True:
            user.is_teacher = True
            teacher.create(data.get('teacher', {}), user)
        user.save()




class teacher(models.Model):
    subjects = models.ManyToManyField(Subject)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

    @staticmethod
    def create(data : dict, user : User):
        teacher = teacher()
        teacher.user = user
        subjects = data.get("subjects", tuple())
        for subject_id in subjects:
            teacher.subjects.add(subject.objects.get(pk=subject_id))
        new_subjects = data.get("new_subjects", tuple())
        for subject_name in new_subjects:
            subject = subject.objects.get_or_create(name=subject_name)
            teacher.subjects.add(subject)
        teacher.save()


class student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='student', blank=True, null=True)


    @staticmethod
    def create(data : dict, user : User):
        student = student()
        student.user = user
        grade = grade.getGrade(data)
        student.save()



class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=50, blank=True)


class MediaStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(MediaPost, on_delete=models.PROTECT)
