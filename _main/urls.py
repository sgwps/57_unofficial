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
from news.views import *
from news_creation.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='Главная'),
    path('quill_test/', QuillView.as_view(), name="Quill"),
    path('article_in_progress', ArtcleWorkAPI.as_view()),
    path('publish', NewsPublication.as_view()),
    path('news', Articles.as_view()),
    path('articles-json/<int:num_posts>/', ArticlesJsonListView.as_view()),
    path('publication', PublicationView.as_view())
]
