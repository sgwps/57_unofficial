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
    context = {
        'general_reg_form': general_reg_form,
        'student_reg_form' : student_reg_form,
        'grade_form' : grade_form
    }

    def get(self, request, *args, **kwargs):
        return render(request, Registration.template_name, context=Registration.context)


    def post(self, request, *args, **kwargs):
        general_reg_form_post = Registration.general_reg_form(request.POST)
        if general_reg_form_post.is_valid():
            user = general_reg_form_post.save()
            return HttpResponse("done")
        post_error_context = {
            'general_reg_form' : general_reg_form_post
        }
        return render(request, Registration.template_name, context=post_error_context)



class GradesAPI(APIView):
    def get(self, request):
        year = request.GET['year']
        return Response(models.Grade.getGradesByYear(year))

