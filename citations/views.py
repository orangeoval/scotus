from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scotus import settings
from citations.models import Citation
from discovery.Url import Url
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import VerifyCitationForm

def index(request):
    template = 'citations.html'

    context = {
        'citations': Citation.objects.all().order_by('-opinion__id'),
        'WEBCITE': settings.WEBCITE,
    }

    return render(request, template, context)

def justice_opinions_citations(request, justice_id):
    template = 'citations.html'

    # Check if filtering by link status instead of justice_id 
    if justice_id in [status for code, status in Citation.STATUSES]:
        return get_citations_by_status(request, justice_id)

    else:
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

@login_required()
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
                    citation.get_statuses()

                # If WEBCITE is enabled in settings.py and validated url is non-404, archive the
                # validated url through WebCite service: http://www.webcitation.org
                if settings.WEBCITE and citation.status != 'u':
                    from requests import post
                    import xml.etree.ElementTree as ET

                    #TODO: add opinion/citation/scotus app info to metadata fields
                    archive = '%s?returnxml=true&url=%s&email=%s' % (settings.WEBCITE_ARCHIVE, 
                                                                     validated,
                                                                     settings.CONTACT_EMAIL)
                    response = post(archive)
                    xml = response.text
                    root = ET.fromstring(xml)
            
                    #TODO: should handle failure here more properly?
                    try:
                        citation.webcite = root.findall('resultset')[0].findall('result')[0].findall('webcite_url')[0].text
                    except:
                        pass

                citation.verify_date = timezone.now()
                citation.validated = validated
                citation.scrape_evaluation = scrape_evaluation
                citation.save()

                return HttpResponseRedirect('/citations/#%s' % citation.id)

            # Submitted invalidated url
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
            form = VerifyCitationForm(
                initial = {
                    'validated': citation.scraped,
                }
            )
            context = {
                'citation': citation,
                'form': form,
            } 
        except Exception:
            return redirect(request)

    return render(request, template, context)

def get_citations_by_status(request, status):
    template = 'citations.html'
    citations = Citation.objects.filter(status=status[0])
    context = {
        'citations':citations,
    }

    return render(request, template, context)

def redirect(request, *args):
    return HttpResponseRedirect('/citations/')
