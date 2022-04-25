from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from . import models
from . import forms
import json
from django.contrib.auth.models import User
from rest_framework.response import Response




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
        general_reg_form_post = Registration.general_reg_form(request.POST)
        student_reg_form_post = Registration.student_reg_form(request.POST)
        grade_form_post = Registration.grade_form(request.POST)
        teacher_reg_form_post = Registration.teacher_reg_form(request.POST)
        # collect form for error
        if general_reg_form_post.is_valid():
            user = general_reg_form_post.save()
            student = None
            if request.POST.get('is_student') == 'on':
                user.is_student = True
                student_reg_form_cleaned = student_reg_form_post.cleaned_data()
                student_reg_form_cleaned['grade'] = request.POST.get('grade')
                grade_form_cleaned = grade_form_post.cleaned_data()
                
                models.Student.create(user, student_reg_form_cleaned, grade_form_cleaned)
            if request.POST.get('is_teacher') == 'on': 
                pass  
            user.save 
            return HttpResponse("done")
        return HttpResponse("not hehe")
        #return render(request, Registration.template_name, context=post_error_context)



class GradesAPI(APIView):
    def get(self, request):
        year = request.GET['year']
        return Response(models.Grade.getGradesByYear(year))

