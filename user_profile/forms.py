from django import forms


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


class StudentRegistrationForm(forms.Form):
    end_year = forms.IntegerField()
    grade_letter = forms.CharField(max_length=1)


class TeacherRegistrationForm(forms.Form):
    subject = forms.CharField(max_length=50)
