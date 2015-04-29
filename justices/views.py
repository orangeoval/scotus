from django.shortcuts import render
from justices.models import Justice

def index(request):
    template = 'justices.html'

    context = {
        'justices': Justice.objects.all(),
    }

    return render(request, template, context)
