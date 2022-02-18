from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.html import format_html

from templates import *
# Create your views here.
def test_reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
    content = {'text' : format_html("This is normal text - <b>and this is bold text</b>.")}

    return render(request, 'reg_test.html', content)
