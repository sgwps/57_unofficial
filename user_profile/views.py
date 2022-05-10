import json
from multiprocessing import get_context
from re import template
from django.http import HttpResponse 
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from . import models
from . import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from multiprocessing import context
from re import template
import re
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class Login(View):
    temlpate_name = 'login.html'
    login_form = forms.LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('../')
        ctx = {'login_form': Login.login_form(), 'error': ''}
        return render(request, Login.temlpate_name, ctx)

    def post(self, request, *args, **kwargs):
        login_form = Login.login_form(request.POST)
        ctx = {'login_form': Login.login_form(), 'error': ''}

        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('../')
                else:
                    ctx['error'] = 'Disabled account'
                    return render(request, Login.temlpate_name, ctx)
            else:
                ctx['error'] = 'Invalid login'
                return render(request, Login.temlpate_name, ctx)
        return render(request, Login.temlpate_name, {'login_form': Login.login_form()})


class ProfileSetting(View):

    @staticmethod
    def saveStudent(student_reg_form_cleaned, grade_form_cleaned, user):
        grade = models.Grade.getGrade(student_reg_form_cleaned, grade_form_cleaned)
        student = models.Student.objects.get_or_create(user=user)[0]
        student.grade = grade
        student.save()


    @staticmethod
    def getSubjectList(request, teacher_reg_form_cleaned):
        subjects = list()
        for item in teacher_reg_form_cleaned.get("subjects"):
            subjects.append(item)
        for key in request.POST.keys():
            if key[:15] == "another_subject":
                subject_name = request.POST[key].capitalize()
                if len(subject_name) != 0:
                    subjects.append(models.Subject.objects.get_or_create(name=subject_name)[0])
        return subjects





class Registration(View):
    template_name = 'registration.html'
    general_reg_form = forms.BasicRegistrationForm
    student_reg_form = forms.StudentRegistrationForm
    grade_form = forms.CustomGradeForm
    teacher_reg_form = forms.TeacherRegistrationForm
    context = {
        'general_reg_form': general_reg_form,
        'student_reg_form' : student_reg_form,
        'grade_form' : grade_form,
        'teacher_reg_form' : teacher_reg_form
    }

    def get(self, request, *args, **kwargs):
        return render(request, Registration.template_name, context=Registration.context)


    def post(self, request, *args, **kwargs):
        general_reg_form_post = Registration.general_reg_form(request.POST, request.FILES)
        student_reg_form_post = Registration.student_reg_form(request.POST)
        grade_form_post = Registration.grade_form(request.POST)
        teacher_reg_form_post = Registration.teacher_reg_form(request.POST)
        # collect form for error
        if general_reg_form_post.is_valid():
            user = general_reg_form_post.save(commit=False)
            user.set_password(general_reg_form_post.cleaned_data["password"])
            if models.UnregisterdUser.objects.filter(email=user.email).exists():
                user.is_confirmed = True
                models.UnregisterdUser.objects.filter(email=user.email).delete()

            user.save()
            student = None
            if request.POST.get('is_student') == 'on':
                if student_reg_form_post.is_valid() and grade_form_post.is_valid():
                    user.is_student = True
                    student_reg_form_cleaned = student_reg_form_post.cleaned_data
                    student_reg_form_cleaned['grade'] = request.POST.get('grade')
                    grade_form_cleaned = grade_form_post.cleaned_data
                    ProfileSetting.saveStudent(student_reg_form_cleaned, grade_form_cleaned, user)
                else:
                    return HttpResponse("error")
            if request.POST.get('is_teacher') == 'on': 
                user.is_teacher = True
                if teacher_reg_form_post.is_valid():
                    subjects = ProfileSetting.getSubjectList(request, teacher_reg_form_post.cleaned_data)
                    models.Teacher.create(user, subjects)
                else:
                    return HttpResponse("error")
            user.save() 
            return HttpResponse("done")
        return HttpResponse("not hehe")
        #return render(request, Registration.template_name, context=post_error_context)



class GradesAPI(APIView):
    def get(self, request):
        year = request.GET['year']
        return Response(models.Grade.getGradesByYear(year))


class ModerationInvite(View):
    template_name = 'email_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, ModerationInvite.template_name)


    def post(self, request, *args, **kwargs):
        for key in request.POST.keys():
            if key[:13] == 'another_email':
                email = request.POST[key]
                new_user = models.UnregisterdUser.objects.get_or_create(email=email)
                new_user.save()
        return redirect('../')
 

class ChangeData(View):

    template_name = 'change_profile.html'
    general_reg_form = forms.ChangeRegistrationData
    student_reg_form = forms.StudentRegistrationForm
    grade_form = forms.CustomGradeForm
    teacher_reg_form = forms.TeacherRegistrationForm
    context = {
        'basic_profile': general_reg_form,
        'student_reg_form' : student_reg_form,
        'grade_form' : grade_form,
        'teacher_reg_form' : teacher_reg_form,
        'student_data' : None
    }


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context_get = ChangeData.context
            context_get['basic_profile'] = forms.ChangeRegistrationData(instance=request.user)
            if request.user.is_student == True:
                student = models.Student.objects.get(user=request.user)
                grade = student.grade
                if grade != None:
                    context_get['end_year'] = grade.graduation_year
                    context_get['grade'] = grade.id

            if request.user.is_teacher == True:
                teacher = models.Teacher.objects.get(user=request.user)
                context_get['teacher_reg_form'] = forms.TeacherRegistrationForm(instance=teacher)
            return render(request, ChangeData.template_name, context=context_get)


    def post(self, request, *args, **kwargs):
        general_reg_form_post = ChangeData.general_reg_form(request.POST, request.FILES, instance=request.user)
        student_reg_form_post = ChangeData.student_reg_form(request.POST)
        grade_form_post = ChangeData.grade_form(request.POST)
        teacher_reg_form_post = ChangeData.teacher_reg_form(request.POST)
        # collect form for error

        if general_reg_form_post.is_valid():
            user = general_reg_form_post.save()
            if user.is_student == True:
                if student_reg_form_post.is_valid() and grade_form_post.is_valid():
                    student_reg_form_cleaned = student_reg_form_post.cleaned_data
                    student_reg_form_cleaned['grade'] = request.POST.get('grade')
                    grade_form_cleaned = grade_form_post.cleaned_data
                    ProfileSetting.saveStudent(student_reg_form_cleaned, grade_form_cleaned, user)

                else:
                    return HttpResponse("error")
            else:
                models.Student.objects.filter(user=user).delete()
            if user.is_teacher == True: 
                if teacher_reg_form_post.is_valid():
                    subjects = ProfileSetting.getSubjectList(request, teacher_reg_form_post.cleaned_data)
                    teacher = models.Teacher.objects.get_or_create(user=user)[0]
                    teacher.subjects.clear()
                    teacher.subjects.add(*subjects)
                else:
                    return HttpResponse("error")
            else:
                models.Teacher.objects.filter(user=user).delete()

            user.save() 
            return HttpResponse("done")
        print(general_reg_form_post.errors)
        return HttpResponse("not hehe")


def CheckUsename(request):
    username = request.GET['username']
    print(username)
    result = {'result':True}
    if models.User.objects.filter(username=username).exists() and username != "":
        result['result'] = False
    return JsonResponse(result)


def CheckEmail(request):
    email = request.GET['email']
    result = {'result':True}
    print(email)
    if models.User.objects.filter(email=email).exists() and email != "":
        result['result'] = False
    return JsonResponse(result)



class Profile(View):
    template_profile_page = 'profile_page.html'
    def get(self, request, *args, **kwargs):
        ctx = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }
        return render(request, Profile.template_profile_page, ctx)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect('index')