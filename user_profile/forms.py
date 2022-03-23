from datetime import datetime
from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
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
    def get_grades(self):
        print(self.end_year)

    end_year = forms.IntegerField(widget = forms.TextInput(
        attrs={
            'id': 'end-year',
            'min':1940,
            'max':get_max_year()
        }
    ), min_value=1940, max_value=get_max_year())
    grade_letter = forms.ChoiceField(required=False)






class TeacherRegistrationForm(forms.Form):
    subject = forms.CharField(max_length=50)
