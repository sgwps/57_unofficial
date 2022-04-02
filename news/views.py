from django.shortcuts import render


def test_header(request):
    return render(request, 'header_test.html')
