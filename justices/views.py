from django.shortcuts import render
from justices.models import Justice
from opinions.models import Opinion
from citations.models import Citation

def index(request):
    template = 'justices.html'
    justices = Justice.objects.all()

    for justice in justices:

        justice.opinion_count = Opinion.objects.filter(justice_id=justice.id).count()
        justice.citation_count = Citation.objects.filter(opinion_id__justice_id=justice.id).count()
        if justice.citation_count:
            justice.average_count = justice.citation_count / float(justice.opinion_count)
        else:
            justice.average_count = 0
 
    context = {
        'justices': justices,
    }

    return render(request, template, context)
