from django.shortcuts import render
from citations.models import Citation

def index(request):
    template = 'citations.html'

    context = {
        'citations': Citation.objects.all().order_by('-opinion__id'),
    }

    return render(request, template, context)

def justice_opinions_citations(request, justice_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id__justice_id=justice_id)

    context = {
        'citations': citations,
    }

    return render(request, template, context)

def opinion_citations(request, opinion_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id=opinion_id)

    context = {
        'citations':citations,
    }

    return render(request, template, context)
