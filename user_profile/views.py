from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from . import models
from . import forms
import json


class UserRegistration(View):
    template_name = 'registration.html'
    general_reg_form = forms.RegistrationForm
    student_reg_form = forms.StudentRegistrationForm
    teacher_reg_form = forms.TeacherRegistrationForm
    custom_profile_form = forms.CustomProfileForm
    context = {
        'general_reg_form': general_reg_form(),
        'student_reg_form': student_reg_form(),
        'teacher_reg_form': teacher_reg_form(),
        'custom_profile_form': custom_profile_form()
    }

    def get(self, request, *args, **kwargs):
        return render(request, UserRegistration.template_name, context=UserRegistration.context)

    def post(self, request, *args, **kwargs):
        result = {}
        general_form = UserRegistration.general_reg_form(request.POST)
        student_form = UserRegistration.student_reg_form(request.POST)
        teacher_form = UserRegistration.teacher_reg_form(request.POST)
        custom_profile_form = UserRegistration.custom_profile_form(request.POST)


        if general_form.is_valid():
            result['profile'] = {
                'Gender': general_form.cleaned_data['gender'],
                'Birthday': general_form.cleaned_data['birth_date']
            }

            result['user'] = {
                'username': general_form.cleaned_data['username'],
                'first_name': general_form.cleaned_data['name'],
                'last_name': general_form.cleaned_data['surname'],
                'email': general_form.cleaned_data['email'],
                'password': general_form.cleaned_data['password']
            }

            if student_form.is_valid():
                result['is_student'] = True
                result['student'] = {
                    'graduation_year': student_form.cleaned_data['end_year']
                }
                if student_form.cleaned_data['grade_letter'] == 'other':
                    #save new grade
                    result['student']['grade_letter'] = custom_profile_form.cleaned_data['custom_grade_letter']
                else:
                    result['student']['grade_letter'] = student_form.cleaned_data['grade_letter'][0]
            else:
                result['is_student'] = False

            if teacher_form.is_valid():
                result['is_teacher'] = True
                result['teacher'] = {
                    'subject': teacher_form.cleaned_data['subject']
                }
            else:
                result['is_teacher'] = False
            return JsonResponse(result)
        return render(request, UserRegistration.template_name, context=UserRegistration.context)



def su2(request):
    return HttpResponse(models.Specialization.get_form_content())