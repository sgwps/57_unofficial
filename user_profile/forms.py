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


class StudentRegistrationForm(forms.Form):
    end_year = forms.IntegerField(widget = forms.TextInput(
        attrs={
            'id': 'end-year'
        }
    ))
    grade_letter = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={
                'id': 'grade-letter'
            }
    ))


class TeacherRegistrationForm(forms.Form):
    subject = forms.CharField(max_length=50)
