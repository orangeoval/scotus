from django.shortcuts import render

def index(request):
    template = 'authors.html'
    context = {'template': template};
    return render(request, template, context)
