from django.shortcuts import render


def page_code_403(request):
    template = 'mysite/page_code_403.html'
    return render(request, template)
