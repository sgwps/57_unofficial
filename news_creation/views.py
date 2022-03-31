from distutils.command.upload import upload
from email.policy import default
from django.http import HttpResponse
from django.shortcuts import render
from news_creation.forms import NewsCreationForm
from news_creation.forms import QuillFieldForm
from news_creation.models import Article
from datetime import datetime
# Create your views here.

def creation(request):
    form_valid = True
    
    if request.method == 'POST':
        f = NewsCreationForm(request.POST)
        if f.is_valid:
            pass
        else:
            form_valid = False
    else:
        f = NewsCreationForm()
    
    ctx = {
        'form': f,
        'form_valid': form_valid
    }
    
    return render(request, 'news_creation.html', context = ctx)


def form_view(request):
    
    if request.method == "POST":
        form = QuillFieldForm(request.POST)
        print('POST:', request.GET.get('id', default=0))
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
            # if article.in_progress == False:
            form = QuillFieldForm(initial={'content': article.content})
            article.save()
            return render(request, 'Quill.html', {'form': form})
            '''else:
                return HttpResponse("this article is in work")'''
#если пользователь закрыл окно с редактором а не отправил на сервер - все еще ин прогресс
