from django.shortcuts import render
from news_creation.forms import NewsCreationForm
from .forms import QuillFieldForm
# Create your views here.

def creation(request):
    form_valid = True
    
    if request.method == 'POST':
        f = NewsCreationForm(request.POST)
        if f.is_valid:
            
            """
            Создаем json
            
            {
                "1":{
                    "text": "lorem ipsum",
                    "img": "images/fayer_1"
                }, //изображение с подписью внизу
                "2":{
                    "img": "images/fayer_2"
                }, //изображение без подписи
                "3":{
                    "text": "lorem ipsum" 
                }, //параграф текста
                "4":{
                    "text": "normal <b>bold text</b>"
                },
                "5":{
                    "text": "normal <i>italic text</i>"
                }
            }
            """
            
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
    return render(request, 'Quill.html', {'form': QuillFieldForm()})
