from distutils.command.upload import upload
from email.policy import default
from django.http import HttpResponse
from django.shortcuts import render
from news_creation.forms import NewsCreationForm
from news_creation.forms import QuillFieldForm
from news_creation.models import Article
from datetime import datetime


# Create your views here.


def form_view(request):
    if request.method == "POST":
        form = QuillFieldForm(request.POST)
        print('POST:', request.GET.get('id', default=0))
        if form.is_valid():
            id = request.GET.get('id', default=0)
            if id == 0:
                quill = Article(
                    content=form.cleaned_data['content'],
                    date_created=datetime.now(),
                    uploaded=False,
                    in_progress=False
                )
                quill.save()
            else:
                article = Article.objects.get(pk=id)
                article.in_progress = False
                article.content = form.cleaned_data['content']
                article.save()
            return HttpResponse("done")
        return HttpResponse("not hehe")

    else:
        print(request.GET)
        id = request.GET.get('id', default=0)
        if id == 0:
            form = QuillFieldForm()
            return render(request, 'Quill.html', {'form': form})
        else:
            article = Article.objects.get(pk=id)
            if not article.in_progress:
                form = QuillFieldForm(initial={'content': article.content})
                article.in_progress = True
                article.save()
                return render(request, 'Quill.html', {'form': form})
            else:
                return HttpResponse("this article is in work")

# если пользователь закрыл окно с редактором а не отправил на сервер - все еще ин прогресс
