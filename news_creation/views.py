import json
from datetime import datetime, timezone
from rest_framework.views import APIView
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from news_creation.forms import QuillFieldForm
from news_creation.models import Article
from news import models as NewsModels
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required   
from user_profile import models as UserModels


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
        if request.user.is_media_staff == True:
            article_id = request.GET.get('id', default=0)
            if article_id == 0:
                return render(request, QuillView.template_name, QuillView.context)
            article = Article.objects.get(pk=article_id)
            now = datetime.now(timezone.utc)
            if article.time_flag is None or (abs(article.time_flag - now).total_seconds() > 40):
                get_context = QuillView.context.copy()
                get_context['form'] = QuillFieldForm(initial={'content': article.content})
                article.time_flag = datetime.now()
                article.save()
                return render(request, QuillView.template_name, get_context)
            return HttpResponse("this article is in work")
        return HttpResponseForbidden()


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
        if request.user.is_media_staff:
            if UserModels.MediaStaff.objects.filter(user=request.user)[0].post.access_to_publish == True:
                html_code = BeautifulSoup(json.loads(request.POST['content'])['html'], features="html.parser")
                new_article = NewsModels.Article(
                    content = str(html_code),
                    date_created=datetime.now()
                )
                new_article.save()
                article_id = request.POST.get('id')
                print(article_id)
                if article_id != 0:
                    Article.objects.get(pk=article_id).delete()
                return HttpResponse("published")

        return HttpResponseForbidden()



class ArticlesJsonListView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_posts')
        lower = upper - 1
        articles = list(NewsModels.Article.objects.values()[lower:upper])
        articles_size = len(NewsModels.Article.objects.all())
        max_size = True if upper >= articles_size else False
        return JsonResponse({'data': self.parse_articles(articles), 'max': max_size}, safe=False)

    def parse_articles(self, articles_list, *args, **kwargs):
        data = []
        for article in articles_list:
            html_code = BeautifulSoup(article['content'], features="html.parser")
            article_dict = {}

            article_dict['header'] = html_code.h1
            if not article_dict.get('header'):
                article_dict['header'] = html_code.h2
            if not article_dict.get('header'):
                article_dict['header'] = html_code.h3

            try:
                article_dict['image'] = html_code.find('img')['src']
            except TypeError:
                pass
            try:
                article_dict['header'] = article_dict['header'].string
            except AttributeError:
                pass
            article_dict['id'] = article['id']
            data.append(article_dict)
        return data


class Articles(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news.html")
