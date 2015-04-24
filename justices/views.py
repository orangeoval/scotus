from django.shortcuts import render

def index(request):
    template = 'justices.html'
    context = {'template': template};
    return render(request, template, context)
