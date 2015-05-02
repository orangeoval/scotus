# -*- coding: utf-8 -*-

from django.shortcuts import render

def overview(request):
    template = 'overview.html'
    return render(request, template)

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
