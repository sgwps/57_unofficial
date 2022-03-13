from django.contrib import admin
from .models import QuillPost

# Register your models here.
# Это необязательно, но сделано для проверки, ссылка на гит где нашёл :
# https://github.com/LeeHanYeong/django-quill-editor
@admin.register(QuillPost)
class QuillPostAdmin(admin.ModelAdmin):
    pass