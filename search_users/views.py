import json
from multiprocessing import get_context
from re import template
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

import user_profile
from rest_framework.views import APIView
from rest_framework.response import Response
from multiprocessing import context
from re import template
import re
from urllib import request
from user_profile.models import *

from django.shortcuts import render, redirect

# Create your views here.
class SearchMain(View):

    def get(self, request, *args, **kwargs):
        return render(request, "search.html")

class UsersAPI(APIView):
    def get(self, request):
        main = request.GET['main'].split()
        users = set()
        for word in main:
            users.update(user_profile.models.User.objects.filter(username=word))
            users.update(user_profile.models.User.objects.filter(first_name=word))
            users.update(user_profile.models.User.objects.filter(last_name=word))
        response = dict()
        response['response'] = list()
        for user in users:
            response['response'].append({
                "username" : user.username,
                "first_name" : user.first_name,
                "last_name" : user.last_name
            })
        print(response)
        return JsonResponse(response)


