from django.shortcuts import render
from news_creation.models import Article
from django.views.generic import View, TemplateView
from .models import NewsTest
from django.http import JsonResponse


class MainView(TemplateView):
    template_name = "news.html"


class ArticlesJsonListView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_posts')
        lower = upper - 1
        articles = list(NewsTest.objects.values()[lower:upper])
        articles_size = len(NewsTest.objects.all())
        max_size = True if upper >= articles_size else False
        return JsonResponse({'data': articles, 'max': max_size}, safe=False)


def main_page(request):
    return render(request, 'main_page.html')


def show_smth(request):
    content = Article.objects.all()
    return render(request, 'test.html', {"content": content})

def news(request):
    return render(request, 'news.html')
