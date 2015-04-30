from django.shortcuts import render
from citations.models import Citation
from django.http import HttpResponseRedirect

def index(request):
    template = 'citations.html'

    context = {
        'citations': Citation.objects.all().order_by('-opinion__id'),
    }

    return render(request, template, context)

def justice_opinions_citations(request, justice_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id__justice_id=justice_id)

    if not citations:
        return redirect(request)

    context = {
        'citations': citations,
    }

    return render(request, template, context)

def opinion_citations(request, opinion_id):
    template = 'citations.html'
    citations = Citation.objects.filter(opinion_id=opinion_id)

    if not citations:
        return redirect(request)

    context = {
        'citations':citations,
    }

    return render(request, template, context)

def verify(request, citation_id):
    template = 'verify.html'

    try:
        citation = Citation.objects.get(id=citation_id)
    except Exception:
        return redirect(request)

    context = {
        'citation': citation,
    }

    return render(request, template, context)

def redirect(request, *args):
    return HttpResponseRedirect('/citations/')
