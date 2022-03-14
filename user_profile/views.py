import json

from django.http import JsonResponse
from django.shortcuts import render
from . import models
# Create your views here.
from django.views import View
from . import forms

"""
In case of OurUser problems modify this not stolen code:
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
"""


def sign_up(request):
    if request.method == 'POST':
        print(1111)
    return render(request, 'registration.html')


def su2(request):
    with open('user_profile/test.json') as json_file:
        data = json.load(json_file)
        models.Profile.create(data)
    return render(request, "reg2.html")

class Index(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        return render(request, Index.template_name, {'email': request.GET.get('email')})


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
        return render(request, 'reg3.html', context=UserRegistration.context)

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
            return render(request, 'reg3.html', context=UserRegistration.context)
