from django import forms
import django.core.validators as validators
from datetime import datetime


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    username = forms.CharField(max_length=50)
    birth_date = forms.DateField()
    gender = forms.ChoiceField(choices=(
        ("male", "Мужской"),
        ("female", "Женский")
    ))


def get_max_year():
    date = datetime.now().year
    return date + 11



class StudentRegistrationForm(forms.Form):
    end_year = forms.IntegerField(min_value=1940, max_value=get_max_year())
    grade_letter = forms.CharField(max_length=1)


class TeacherRegistrationForm(forms.Form):
    subject = forms.CharField(max_length=50)
