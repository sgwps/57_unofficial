"""_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import user_profile.views
from django.http import JsonResponse
from django.views.generic import TemplateView
import news_creation.views


def get_grades(request):
    print(request.GET['year'])
    return JsonResponse({"А":123, "Б":124})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_profile.views.Login.as_view()),
    path('signup/', user_profile.views.Registration.as_view()),
    path('grades_api/', user_profile.views.GradesAPI.as_view()),
    path('', TemplateView.as_view(template_name="main.html")),
    path('quill_test/', news_creation.views.QuillView.as_view(), name="Quill"),
    path('article_in_progress', news_creation.views.ArtcleWorkAPI.as_view()),
    path('publish', news_creation.views.NewsPublication.as_view())
]
