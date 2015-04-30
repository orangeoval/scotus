from django.shortcuts import render
from justices.models import Justice
from opinions.models import Opinion
from citations.models import Citation

def index(request):
    template = 'justices.html'
    justices = Justice.objects.all()

    for justice in justices:
        justice.get_counts()
 
    context = {
        'justices': justices,
    }

    return render(request, template, context)

def justice_opinions(request, justice_id):
    template = 'opinions.html'
    opinions = Opinion.objects.filter(justice_id=justice_id)

    for opinion in opinions:
        opinion.get_counts_and_update_date()

    context = {
        'opinions': opinions,
    }

    return render(request, template, context)

def justice_opinions_citations(request, justice_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id__justice_id=justice_id)

    context = {
        'citations': citations,
    }

    return render(request, template, context)
