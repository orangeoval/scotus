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
    from django.db.models import Count
    from datetime import timedelta

    template = 'overview.html'
    chartID = 'chart_temporal_distribution'
    chart_type = 'line'
    chart_height = 400
    js_month = 2678400000
    nyt_publication = 1379995200000
   
    # Get citation counts by date
    data = []
    opinions = Opinion.objects.values('published').annotate(citation_count=Count('citation'))
    for opinion in opinions:
        unix_date = int(opinion['published'].strftime('%s')) 
        js_date = unix_date * 1000
        data.append([js_date, opinion['citation_count']])

    # Get earliest and latest date, plus/minus 1 month
    sorted_data = sorted(data, key=lambda x: x[0])
    earliest = sorted_data[0][0] - js_month
    latest = sorted_data[-1][0] + js_month

    context = {
        'chartID': chartID,
        'chart': {
            'renderTo': chartID,
            'type': chart_type,
            'height': chart_height,
        },
        'title': {
            'text': '',
        },
        'xAxis': {
            'type': 'datetime',
            'min': earliest,
            'max': latest,
            'title': {
                'text': 'date',
            },
            'plotLines': [
                {
                    'color': '#58FA82',
                    'dashStyle': 'dot',
                    'value': nyt_publication,
                    'width': 2,
                },
            ],
        },
        'yAxis': {
            'title': {
                'text': '',
            },
        },
        'series': [
            {
                'name': 'Web Citations',
                'data': data,
            },
        ],
    }

    return render(request, template, context)
