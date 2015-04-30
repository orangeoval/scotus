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
