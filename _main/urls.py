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


def get_grades(request):
    print(request.GET['year'])
    return JsonResponse({"А":123, "Б":124})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', user_profile.views.BasicRegistration.as_view()),
    path('signup2/', user_profile.views.su2),
    path('login/', user_profile.views.Login.as_view()),
    path('get_grades/', user_profile.views.GetGrades),
    path('get_subjects', user_profile.views.GetSubjects),
    path('check_username', user_profile.views.CheckUsename),
    path('check_email', user_profile.views.CheckEmail),
    path('get_specializations', user_profile.views.GetSpecializations),
    path('', TemplateView.as_view(template_name="main.html"))
]
