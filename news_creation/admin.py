from django.contrib import admin
from .models import Saved_data

# Register your models here.
# Это необязательно, но сделано для проверки, ссылка на гит где нашёл :
# https://github.com/LeeHanYeong/django-quill-editor
@admin.register(Saved_data)
class QuillPostAdmin(admin.ModelAdmin):
    pass