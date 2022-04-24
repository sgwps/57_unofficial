from django.shortcuts import render
from news_creation.models import Article
from bs4 import BeautifulSoup

# Create your views here.


def main_page(request):
    return render(request, 'main_page.html')

"""
def show_smth(request):
    return preview((request))
    # content = Article.objects.all()
    # return render(request, 'test.html', {"content": content})
"""

def news(request):
    return render(request, 'news.html')


def show_smth(request):
    content = Article.objects.all()
    cnt = []
    k=0
    for i in content:
        apendix = []
        soup = BeautifulSoup(i.content.html,'html.parser')
        # paragraph = soup.p
        # apendix.append(paragraph)
        image = soup.img
        apendix.append(image)
        header1 = soup.h1
        if header1 is None:
            Header = soup.h2
            if Header is None:
                header = soup.h3
                apendix.append(header)
            else:
                apendix.append(Header)
        else:
            apendix.append(header1)
        cnt.append(apendix)
        k += 1
    print(cnt)
    #print(content)

    return render(request, 'test.html', {"content": cnt[::-1]})



"""     item = soup.p
        item2 = soup.img
        #print(item)
        print(item2)
"""