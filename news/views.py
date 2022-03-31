from django.shortcuts import render


# Create your views here.

def main_page(request):
    return render(request, 'main_page.html')


def news(request):
    return render(request, 'news.html')
