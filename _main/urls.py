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
import news.views
from django.contrib import admin
from django.urls import path
from news_creation.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news.views.main_page, name='Главная'),
    path('quill_test/', form_view, name="Quill"),
    path('news/', news.views.MainView.as_view(), name='Новости'),
    path('news/articles-json/<int:num_posts>/', news.views.ArticlesJsonListView.as_view()),
    path('test/', news.views.show_smth),
]
