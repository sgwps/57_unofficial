from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from . import forms


class UserRegistration(View):
    general_reg_form = forms.RegistrationForm
    student_reg_form = forms.StudentRegistrationForm
    teacher_reg_form = forms.TeacherRegistrationForm
    context = {
        'general_reg_form': general_reg_form(),
        'student_reg_form': student_reg_form(),
        'teacher_reg_form': teacher_reg_form()
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'registration.html', context=UserRegistration.context)

    def post(self, request, *args, **kwargs):
        general_form = UserRegistration.general_reg_form(request.POST)
        student_form = UserRegistration.student_reg_form(request.POST)
        teacher_form = UserRegistration.teacher_reg_form(request.POST)
        if general_form.is_valid():
            result = general_form.cleaned_data
            if student_form.is_valid():
                result = {**result, **student_form.cleaned_data}
            if teacher_form.is_valid():
                result = {**result, **teacher_form.cleaned_data}
            return JsonResponse(result)
        else:
            return render(request, 'registration.html', context=UserRegistration.context)
