import imp
from typing import Any
from django import forms
from ckeditor.fields import RichTextFormField


class NewsCreationForm(forms.Form):
    header = forms.CharField(
        max_length=200,
        label="Заголовок статьи",
        widget=forms.TextInput(attrs={'class': 'form-control'}
    ))
    img = forms.ImageField(
        label="Значок статьи",
        required=False,
        error_messages={'invalid':("Image files only")},
        widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}
    ))
    body = RichTextFormField(label="Текст статьи")
