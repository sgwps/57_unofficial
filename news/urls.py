from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list),
    path('article', views.view_article)
]
