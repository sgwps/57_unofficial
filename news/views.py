from django.shortcuts import render
from news_creation.models import Article

# Create your views here.

def main_page(request):
    return render(request, 'main_page.html')


def show_smth(request):
    content = Article.objects.all()
    return render(request, 'test.html', {"content": content})

def news(request):
    return render(request, 'news.html')
