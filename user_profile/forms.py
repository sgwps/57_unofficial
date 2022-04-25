from dataclasses import fields
from datetime import datetime
import email
from enum import unique
from pyexpat import model
from unittest import result
from django import forms
from . import models
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS


class BasicRegistrationForm(ModelForm):
    
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'birthday', 'gender']
        widgets = {
            'birthday': forms.DateInput(format=('%Y-%m-%d'), 
            attrs={'type': 'date'}) 
        }
        




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
        widget=forms.CheckboxSelectMultiple
    )

