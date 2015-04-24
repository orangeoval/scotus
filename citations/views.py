from django.shortcuts import render

def index(request):
    template = 'citations.html'
    context = {'template': template};
    return render(request, template, context)
