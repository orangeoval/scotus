# -*- coding: utf-8 -*-

from django.shortcuts import render

def download_csv(request):
    from citations.models import Citation
    from django.http import HttpResponse
    from datetime import datetime
    import csv

    fields_header = [
        'Scraped Citation',
        'Validated Citation',
        'Citation Validation Date',
        'Scrape Evaluation',
        'Citation Status',
        'In Library of Congress Web Archive',
        'In Internet Archive Web Archive',
        'Opinion',
        'Justice',
        'Category',
        'Published',
        'Discovered',
        'PDF Url',
        'Reporter',
        'Docket',
        'Part',
    ]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scotus-web-citations.%s.csv' % datetime.now().strftime('%Y%m%d')

    writer = csv.writer(response, delimiter=',')
    writer.writerow(fields_header)

    for citation in Citation.objects.all():
        writer.writerow(citation.csv_row())

    return response


def overview(request):
    from opinions.models import Opinion
    from citations.models import Citation
    from django.db.models import Count
    from datetime import timedelta

    template = 'overview.html'
    js_month = 2678400000
    context = {
        'nyt_publication': 1379995200000,
        'available': Citation.objects.filter(status='a').count(),
        'unavailable': Citation.objects.filter(status='u').count(),
        'redirected': Citation.objects.filter(status='r').count(),
    }

    # Get citation distribution data
    context['citation_distribution'] = []
    for opinion in Opinion.objects.values('published').annotate(citation_count=Count('citation')):
        unix_date = int(opinion['published'].strftime('%s'))
        js_date = unix_date * 1000
        context['citation_distribution'].append([js_date, opinion['citation_count']])

    sorted_data = sorted(context['citation_distribution'], key=lambda x: x[0])
    context['earliest'] = sorted_data[0][0] - js_month
    context['latest'] = sorted_data[-1][0] + js_month

    return render(request, template, context)
