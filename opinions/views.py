from django.shortcuts import render
from opinions.models import Opinion
from citations.models import Citation

def index(request):
    template = 'opinions.html'
    opinions = Opinion.objects.all().order_by('-published')

    for opinion in opinions:
        opinion.get_counts_and_update_date()

    context = {
        'opinions': opinions,
    }

    return render(request, template, context)

def opinion_citations(request, opinion_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id=opinion_id)

    context = {
        'citations':citations,
    }

    return render(request, template, context)
