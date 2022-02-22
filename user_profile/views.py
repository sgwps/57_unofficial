from django.http import HttpResponse
from django.shortcuts import render
from . import forms
# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        print(request)
    form = forms.RegisterForm()
    return render(request, 'sign_up.html', {'form': form})