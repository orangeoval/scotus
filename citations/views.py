from django.shortcuts import render
from citations.models import Citation
from discovery.Url import Url
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import VerifyCitationForm

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

    if request.method == 'POST':
        try:
            # Successful update
            citation = Citation.objects.get(id=request.POST['citation_id'])
            scrape_evaluation = request.POST['scrape_evaluation']
            validated = request.POST['validated']

            form = VerifyCitationForm({
                'validated': validated,
                'scrape_evaluation': scrape_evaluation,
            })

            if form.is_valid():
                # Don't waste time checking validated citation if matched scraped
                if validated != citation.scraped or scrape_evaluation != citation.scrape_evaluation: 
                    status = Url.check_status(validated)
                    citation.set_status(status)

                citation.verify_date = timezone.now()
                citation.validated = validated
                citation.scrape_evaluation = scrape_evaluation
                citation.save()
                return HttpResponseRedirect('/citations/#%s' % citation.id)

            # Didn't submit validated url
            context = {
                'citation': citation,
                'form': form,
            }

        except Exception:
            # Somehow attempted to validate citation not in DB
            context = {
                'error': 'No citation with id %s' % request.POST['citation_id'],
            } 

    else:
        try:
            citation = Citation.objects.get(id=citation_id)
            form = VerifyCitationForm()
            context = {
                'citation': citation,
                'form': form,
            } 
        except Exception:
            return redirect(request)

    return render(request, template, context)

def redirect(request, *args):
    return HttpResponseRedirect('/citations/')
