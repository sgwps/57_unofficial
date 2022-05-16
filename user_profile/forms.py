from dataclasses import fields
from datetime import datetime
from enum import unique
from pyexpat import model
from django import forms
from . import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())


class BasicRegistrationForm(ModelForm):
    
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'birthday', 'gender']
        widgets = {
            'birthday': forms.DateInput(format=('%Y-%m-%d'), 
            attrs={'type': 'date'}),
            'password' : forms.PasswordInput() 
        }
        

class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the 
    e-mail.
    """
    error_messages = {
        'email_mismatch': "The two email addresses fields didn't match.",
        'not_changed': "The email address is the same as the one already defined.",
    }

    new_email1 = forms.EmailField(
        label="New email address",
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label="New email address confirmation",
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


def get_max_year():
    date = datetime.now().year
    return date + 11


def getLetterChoices():
    letters_copy = models.letters.copy()
    result = []
    for i in letters_copy:
        result.append((i, i))
    result.append(('', ''))
    return tuple(result)



class CustomGradeForm(forms.Form):
    custom_grade_letter = forms.ChoiceField(required=False, widget=forms.Select(), choices=getLetterChoices())
    custom_specialization = forms.ChoiceField(required=False, choices=models.Specialization.getTuple)

class StudentRegistrationForm(forms.Form):
    end_year = forms.IntegerField(widget = forms.NumberInput(
        attrs={
            'min':1940,
            'max':get_max_year()
        }
    ), min_value=1940, max_value=get_max_year(), required=False)



class TeacherRegistrationForm(forms.ModelForm):

    class Meta:
        model = models.Teacher
        fields = ['subjects']


    subjects = forms.ModelMultipleChoiceField(
        queryset=models.Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    