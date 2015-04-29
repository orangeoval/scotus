from django.shortcuts import render
from citations.models import Citation

def index(request):
    template = 'citations.html'

    context = {
        'citations': Citation.objects.all().order_by('-opinion__id'),
    }

    return render(request, template, context)
