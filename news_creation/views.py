import json
from datetime import datetime, timezone
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from news_creation.forms import QuillFieldForm
from news_creation.models import Article
from news import models as NewsModels
from bs4 import BeautifulSoup


class QuillView(View):
    template_name = 'Quill.html'
    form = QuillFieldForm
    context = {
        'form' : QuillFieldForm,
        'publishing_allowed' : True
    }

    def post(self, request, *args, **kwargs):
        form = QuillView.form(request.POST)
        if form.is_valid():
            article_id = request.GET.get('id', default=0)
            if article_id == 0:
                quill = Article(
                    content = form.cleaned_data['content'],
                    date_created = datetime.now(),
                )
                quill.save()
            else:
                article = Article.objects.get(pk=article_id)
                article.content = form.cleaned_data['content']
                article.time_flag = None
                article.save()
            return HttpResponse("done")
        return HttpResponse("not hehe")

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('id', default=0)
        if article_id == 0:
            return render(request, QuillView.template_name, QuillView.context)
        article = Article.objects.get(pk=article_id)
        now = datetime.now(timezone.utc)
        if article.time_flag is None or (abs(article.time_flag - now).total_seconds() > 40):
            get_context = QuillView.context
            get_context['form'] = QuillFieldForm(initial={'content': article.content})
            article.time_flag = datetime.now()
            article.save()
            return render(request, QuillView.template_name, get_context)
        return HttpResponse("this article is in work")


class ArtcleWorkAPI(APIView):
    def get(self, request):
        article_id = request.GET.get('id')
        article = Article.objects.get(pk=article_id)
        article.time_flag = datetime.now()
        article.save()
        return HttpResponse(status=200)


class NewsPublication(View):
    form = QuillFieldForm

    def post(self, request, *args, **kwargs):
        form_post = NewsPublication.form(request.POST)
        if form_post.is_valid():
            html_code = BeautifulSoup(json.loads(form_post.cleaned_data['content'])['html'])
            new_article = NewsModels.Publication(
                content = str(html_code),
                is_article = True,
                date_created=datetime.now()
            )
            new_article.save()
            return HttpResponse("published")
        return HttpResponse("no")


class ArticlesJsonListView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_posts')
        lower = upper - 1
        articles = list(NewsModels.Publication.objects.values()[lower:upper])
        articles_size = len(NewsModels.Publication.objects.all())
        max_size = True if upper >= articles_size else False
        return JsonResponse({'data': self.parse_articles(articles), 'max': max_size}, safe=False)

    def parse_articles(self, articles_list, *args, **kwargs):
        data = []
        for article in articles_list:
            html_code = article.content
            article_dict = {}
            article_dict['header'] = html_code.h1.string
            if not article_dict.get('header'):
                article_dict['header'] = html_code.h2.string
            if not article_dict.get('header'):
                article_dict['header'] = html_code.h3.string
            article_dict['image'] = html_code.find('img')['src']
            article_dict['id'] = article['id']
            data.append(article_dict)
        return data


class Articles(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news.html")


class PublicationView(View):
    def get(self, request, *args, **kwargs):
        article = NewsModels.Publication.objects.filter(pk=request.GET.get('id'))[0]
        html_code = article.content
        return render(request, "Publication.html", {'content' : html_code})

        