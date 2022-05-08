from django.contrib import admin
from .models import Article

# Register your models here.
# Это необязательно, но сделано для проверки, ссылка на гит где нашёл :
# https://github.com/LeeHanYeong/django-quill-editor
from django.contrib import admin
from .models import Article

# Register your models here.
# Это необязательно, но сделано для проверки, ссылка на гит где нашёл :
# https://github.com/LeeHanYeong/django-quill-editor
@admin.register(Article)
class QuillPostAdmin(admin.ModelAdmin):
    pass 