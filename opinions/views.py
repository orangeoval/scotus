from django.shortcuts import render
from opinions.models import Opinion
from citations.models import Citation

def index(request):
    template = 'opinions.html'
    opinions = Opinion.objects.all().order_by('-published')

    for opinion in opinions:

        # Get citation counts
        opinion.citation_count = Citation.objects.filter(opinion=opinion.id).count()

        # Get updated sate
        if opinion.updated:
            opinion.updated_date = Opinion.objects.filter(name=opinion.name).latest('published').published


    context = {
        'opinions': opinions,
    }

    return render(request, template, context)
