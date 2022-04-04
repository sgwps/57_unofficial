from datetime import datetime
from django import forms
from . import models


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    birth_date = forms.DateField(widget = forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'type': 'date'}
    ))
    gender = forms.ChoiceField(
        choices=(
            ("male", "Мужской"),
            ("female", "Женский")
        ),
        widget=forms.RadioSelect
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
    ), min_value=1940, max_value=get_max_year())
    grade_letter = forms.ChoiceField(required=False, widget= forms.Select(attrs={'id':'id_grade_letter'}))



class CustomProfileForm(forms.Form):
    custom_grade_letter = forms.ChoiceField(required=False, widget= forms.Select(attrs={'id':'id_grade_letter_other'}))
    # custom_profile = forms.ChoiceField(required=False, choices=models.Specialization.get_form_content())






class TeacherRegistrationForm(forms.Form):
    subject = forms.ImageField()
    # subject = forms.ChoiceField(required=False, choices=models.Specialization.get_form_content(), widget=forms.CheckboxSelectMultiple(attrs={'multiple':'multiple'}))
