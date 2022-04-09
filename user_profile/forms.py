from dataclasses import fields
from datetime import datetime
from enum import unique
from pyexpat import model
from django import forms
from . import models
from django.forms import ModelForm
from django.contrib.auth.models import User




class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    surname = forms.CharField(max_length=50, required=True)
    username = forms.CharField(max_length=50, required=True)  
    email = forms.EmailField(max_length=50, required=True)  
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)  
    birth_date = forms.DateField(
        widget = forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'type': 'date'}
        ), 
        required=False
    )
    gender = forms.ChoiceField(
        choices=models.GetAll(models.Gender), 
        initial='0', 
        required=True
    )

def get_max_year():
    date = datetime.now().year
    return date + 11


class StudentRegistrationForm(forms.Form):
    end_year = forms.IntegerField(widget = forms.NumberInput(
        attrs={
            'id': 'end-year',
            'min':1940,
            'max':get_max_year()
        }
    ), min_value=1940, max_value=get_max_year(), required=False)
    grade_letter = forms.ChoiceField(required=False, widget= forms.Select(attrs={'id':'id_grade_letter'}))



class CustomGradeForm(forms.Form):
    custom_grade_letter = forms.ChoiceField(required=False, widget= forms.Select(attrs={'id':'id_grade_letter_other'}))
    custom_profile = forms.ChoiceField(required=False)






class TeacherRegistrationForm(forms.Form):
    subject = forms.ChoiceField(required=False, widget=forms.CheckboxSelectMultiple(attrs={'multiple':'multiple'}))
