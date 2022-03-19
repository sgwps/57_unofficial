from django.shortcuts import render
from news_creation.forms import NewsCreationForm
from news_creation.forms import QuillFieldForm
from news_creation.models import Saved_data
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
        if form.is_valid():
            quill = Saved_data(
                content = form.cleaned_data['content'],
            )
            quill.save()
    else:
        form = QuillFieldForm()
        
    return render(request, 'Quill.html', {'form': form})
