from django.contrib.auth.models import User
from django.shortcuts import render
from templates import *
# Create your views here.
def test_reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
    return render(request, 'reg_test.html')
