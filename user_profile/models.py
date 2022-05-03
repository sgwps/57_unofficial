from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н' ,'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']


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

    def __str__(self):
        return self.name



class MediaPost(models.Model):
    name = models.CharField(max_length=40, null=True)
    access_to_publish = models.BooleanField()


class Gender(models.Model):  # ISO 5218
    '''
    INSERT INTO user_profile_gender (id, gender) VALUES (0, "not known");
    INSERT INTO user_profile_gender (id, gender) VALUES (1, "male");
    INSERT INTO user_profile_gender (id, gender) VALUES (2, "female");
    #
    INSERT INTO user_profile_gender (id, gender) VALUES (9, "not applicable");
    '''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    graduation_year = models.IntegerField()
    specialization = models.ForeignKey(to=Specialization, on_delete=models.PROTECT, related_name='grades', null=True, blank=True)
    letter = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        unique_together = ('graduation_year', 'letter',)

    @staticmethod
    def getGradesByYear(year : int):
        letters_copy = letters.copy()

        result = list()
        grades_list = Grade.objects.filter(graduation_year=year)
        for grade in grades_list:
            if grade.letter != None:
                specialization = grade.specialization
                tuple = (grade.id, (grade.letter, str(grade.specialization)))
                letters_copy.remove(grade.letter)
                result.append(tuple)
        res_dict = {
            "grades":result,
            "letters":letters_copy
        }
        return res_dict

    @staticmethod
    def getGrade(student_reg_form, grade_form):
        print(student_reg_form, grade_form)
        if student_reg_form.get('end_year') is None:
            return None
        # year not none
        year = student_reg_form.get('end_year')
        if student_reg_form.get('grade', "") == '':
            return Grade.objects.get_or_create(graduation_year=year, letter=None)[0]
        elif student_reg_form.get('grade') == 'other':
            return Grade.objects.get_or_create(
                graduation_year=year,
                letter=grade_form.get('custom_grade_letter'),
                specialization=Specialization.objects.filter(pk=grade_form.get('custom_specialization'))[0],
            )[0]

        else:
            print(int(student_reg_form.get('grade')))
            return Grade.objects.filter(pk=int(student_reg_form.get('grade')))[0]




class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_media_staff = models.BooleanField(default=False)
    gender = models.ForeignKey(to=Gender, on_delete=models.PROTECT, related_name='users', default=0)
    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    bio = models.CharField(blank=True, max_length=1000)
    birthday = models.DateField(blank=True, null=True)
    city = models.IntegerField(blank=True, null=True)




class Teacher(models.Model):
    subjects = models.ManyToManyField(Subject)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

    @staticmethod
    def create(user : User, subjects : list):
        teacher = Teacher()
        teacher.user = user
        teacher.save()
        for subject in subjects:
            teacher.subjects.add(subject)
            print("sub", subject)
        teacher.save()


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    grade = models.ForeignKey(to=Grade, on_delete=models.PROTECT, related_name='student', blank=True, null=True)


    @staticmethod
    def create(user : User, student_reg_form, grade_form):
        student = Student()
        student.user = user
        user.is_student = True
        user.save()
        student.grade = Grade.getGrade(student_reg_form, grade_form)
        student.save()


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=50, blank=True)


class MediaStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(MediaPost, on_delete=models.PROTECT)


