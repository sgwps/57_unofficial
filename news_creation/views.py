from django.shortcuts import render
from news_creation.forms import NewsCreationForm

# Create your views here.

def creation(request):
    form_valid = True
    
    if request.method == 'POST':
        f = NewsCreationForm(request.POST)
        if f.is_valid:
            # Формируем json
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
