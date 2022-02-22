from django import forms
from django.contrib.auth.forms import UserCreationForm
GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('n', 'neutral')
    )
POSITION_CHOICES = (
        ('t', 'teacher'),
        ('s', 'student'),
    )
class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    bio = forms.CharField(max_length=570)
    birthday = forms.DateField()
    position = forms.ChoiceField(choices=POSITION_CHOICES)