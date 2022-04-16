from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from . import models
from . import forms
import json
from django.contrib.auth.models import User



class BasicRegistration(View):
    template_name = 'basic_registration.html'
    general_reg_form = forms.RegistrationForm
    student_reg_form = forms.StudentRegistrationForm
    grade_form = forms.CustomGradeForm
    teacher_form = forms.TeacherRegistrationForm
    context = {
        'general_reg_form': general_reg_form,
        'student_reg_form': student_reg_form,
        'custom_profile_form': grade_form,
        'teacher_reg_form' : teacher_form
    }


    def get(self, request, *args, **kwargs):
        return render(request, BasicRegistration.template_name, context=BasicRegistration.context)


    def post(self, request, *args, **kwargs):
        print(request.POST)
        general_form = BasicRegistration.general_reg_form(request.POST)
        student_form = BasicRegistration.student_reg_form(request.POST)
        grade_form = BasicRegistration.grade_form(request.POST)
        if general_form.is_valid():
            result = dict()
            result['profile'] = {
                'gender': general_form.cleaned_data['gender'],
                'birthday': general_form.cleaned_data['birth_date']
            }

            result['user'] = {
                'username': general_form.cleaned_data['username'],
                'first_name': general_form.cleaned_data['name'],
                'last_name': general_form.cleaned_data['surname'],
                'email': general_form.cleaned_data['email'],
                'password': general_form.cleaned_data['password']
            }
            if student_form.is_valid() and request.POST.get('is_student') == 'on':
                result['is_student'] = True
                result['student'] = {
                    'graduation_year': student_form.cleaned_data['end_year'],
                    'grade_letter' : student_form.cleaned_data['grade_letter']
                }
                if student_form.cleaned_data['grade_letter'] == 'other':
                    result['student']['grade'] = {
                        'custom_grade_letter' : grade_form.cleaned_data['custom_grade_letter'],
                        'custom_profile' : grade_form.cleaned_data['custom_profile']
                    }
            if request.POST.get('is_teacher') == 'on':
                result['is_teacher'] = True
                subjects = []
                new_subjects = []
                for key, value in request.POST.items():
                    if key[:8] == "subject_":
                        subjects.append(int(key[8:]))
                    if key[:15] == "another_subject":
                        if value.capitalize().len() != 0:
                            new_subjects.append(value.capitalize())
                result["teacher"] = {}
                result["teacher"]["subjects"] = subjects
                result["teacher"]["new_subjects"] = new_subjects


            models.Profile.create(result)
            return HttpResponse(str(request.POST))
        return HttpResponse("not hehe")





def su2(request):
    return HttpResponse(models.Specialization.get_form_content())


def GetSubjects(request):
    result = models.GetAll(models.Subject)
    json_response = dict()
    for subject in result:
        json_response[subject[0]] = subject[1]
    return JsonResponse(json_response)


def CheckUsename(request):
    username = request.GET['username']
    print(username)
    result = {'result':True}
    if User.objects.filter(username=username).exists() and username != "":
        result['result'] = False
    return JsonResponse(result)


def CheckEmail(request):
    email = request.GET['email']
    result = {'result':True}
    print(email)
    if User.objects.filter(email=email).exists() and email != "":
        result['result'] = False
    return JsonResponse(result)


def GetGrades(request):
    year = request.GET['year']
    return JsonResponse(models.Grade.GetGradesByYear(year))


def GetSpecializations(request):
    result = models.GetAll(models.Specialization)
    json_response = dict()
    for subject in result:
        json_response[subject[0]] = subject[1]
    return JsonResponse(json_response)
