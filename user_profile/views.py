import json
from django.http import HttpResponse 
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from . import models
from . import forms
from rest_framework.views import APIView
from rest_framework.response import Response
# EMAIL
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings




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
            user = general_reg_form_post.save(commit=False)
            user.set_password(general_reg_form_post.cleaned_data["password"])
            user.save()
            student = None
            if request.POST.get('is_student') == 'on':
                if student_reg_form_post.is_valid() and grade_form_post.is_valid():
                    user.is_student = True
                    student_reg_form_cleaned = student_reg_form_post.cleaned_data
                    student_reg_form_cleaned['grade'] = request.POST.get('grade')
                    grade_form_cleaned = grade_form_post.cleaned_data
                    
                    models.Student.create(user, student_reg_form_cleaned, grade_form_cleaned)
                else:
                    return HttpResponse("error")
            if request.POST.get('is_teacher') == 'on': 
                user.is_teacher = True
                if teacher_reg_form_post.is_valid():
                    subjects = list()
                    for item in teacher_reg_form_post.cleaned_data.get("subjects"):
                        subjects.append(item)
                    for key in request.POST.keys():
                        if key[:15] == "another_subject":
                            subject_name = request.POST[key].capitalize()
                            subjects.append(models.Subject.objects.get_or_create(name=subject_name)[0])
                    models.Teacher.create(user, subjects)
                else:
                    return HttpResponse("error")
            user.save()
            # EMAIL
            if not user.is_active:
                return signup(request, user)
                print('a')

            return HttpResponse("done")
        return HttpResponse("not hehe")
        #return render(request, Registration.template_name, context=post_error_context)



class GradesAPI(APIView):
    def get(self, request):
        year = request.GET['year']
        return Response(models.Grade.getGradesByYear(year))


def signup(request, user):
        form = forms.BasicRegistrationForm(request.POST)
        # email = form.cleaned_data.get('email')
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('new_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
        # to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message,
                  settings.EMAIL_FROM_USER,
                  [user.email])
        print('b')
        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
