from django.shortcuts import render

def index(request):
    template = 'opinions.html'
    context = {'template': template};
    return render(request, template, context)
