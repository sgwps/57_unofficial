from distutils.command.upload import upload
from email.policy import default
from multiprocessing import get_context
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from news_creation.forms import NewsCreationForm
from news_creation.forms import QuillFieldForm
from news_creation.models import Article
from datetime import datetime, timezone, timedelta
from rest_framework.views import APIView
from news import models as NewsModels
# Create your views here.


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
            id = request.GET.get('id', default=0)
            if id == 0:
                quill = Article(
                    content = form.cleaned_data['content'],
                    date_created = datetime.now(),
                )
                quill.save()
            else:
                article = Article.objects.get(pk=id)
                article.content = form.cleaned_data['content']
                article.time_flag = None
                article.save()
            return HttpResponse("done")
        return HttpResponse("not hehe")


    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', default=0)
        if id == 0:
            form = QuillFieldForm()
            return render(request, QuillView.template_name, QuillView.context)
        else:
            article = Article.objects.get(pk=id)
            now = datetime.now(timezone.utc)
            if article.time_flag == None or (abs(article.time_flag - now).total_seconds() > 40):
                get_context = QuillView.context
                get_context['form'] = QuillFieldForm(initial={'content': article.content})
                article.time_flag = datetime.now()
                article.save()
                return render(request, QuillView.template_name, get_context)
            else:
                return HttpResponse("this article is in work")


class ArtcleWorkAPI(APIView):

    def get(self, request):
        id = request.GET.get('id')
        article = Article.objects.get(pk=id)
        article.time_flag = datetime.now()
        article.save()
        return HttpResponse(status=200)

class NewsPublication(View):
    form = QuillFieldForm

    def post(self, request, *args, **kwargs):
        form_post = NewsPublication.form(request.POST)
        if form_post.is_valid():
            new_article = NewsModels.Publication(
                content = form_post.cleaned_data['content'],
                is_article = True,
                date_created=datetime.now()
            )
            new_article.save()
            return HttpResponse("published")
