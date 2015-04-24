from django.shortcuts import render

def index(request):
    page = 'citations.html'
    context = {'page': page};
    return render(request, page, context)
