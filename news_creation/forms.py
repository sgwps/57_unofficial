from django import forms
from django_quill.forms import QuillFormField

class NewsCreationForm(forms.Form):
    header = forms.CharField(max_length=200, label="Введите заголовок")
    img = forms.ImageField(label='Вставьте картинку', required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    paragraph = forms.CharField(label="Параграф", widget=forms.Textarea)


class QuillFieldForm(forms.Form):
    content = QuillFormField()