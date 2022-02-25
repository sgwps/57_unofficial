from django.shortcuts import render
import json
# Create your views here.


def Get_News(request):
    f = str(request.id) +".json"
    with open(f) as data:
        ctx = json.load(data)
    return render(request, 'newsPage.html', context = ctx)

