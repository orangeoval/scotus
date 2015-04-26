# -*- coding: utf-8 -*-

from scotus import settings
from django.utils import timezone

from discovery.Pdf import Pdf
from opinions.models import Opinion
from citations.models import Citation
from justices.models import Justice

import lxml.html
from requests import get
from datetime import datetime


class Discovery:
    def __init__(self):
        self.opinions = []
        self.category_urls = []
        self.pdfs_to_scrape = []
        self.BASE = 'http://www.supremecourt.gov'
        self.OPINIONS_BASE = self.BASE + '/opinions/'
        self.OPINIONS_MAIN_PAGE = self.OPINIONS_BASE + 'opinions.aspx'
        self.YYYYMMDD = timezone.now().strftime('%Y%m%d')

    def run(self):
        self.fetch_opinion_category_urls()
        self.get_opinions_from_categories()
        self.ingest_new_opinions()
        self.ingest_new_citations()

    def get_url(self, url):
        return get(url, headers=settings.REQ_HEADER)

    def fetch_opinion_category_urls(self):
        request = self.get_url(self.OPINIONS_MAIN_PAGE)

        if request.status_code == 200:
            html = lxml.html.fromstring(request.text)
            search = "//div[@class='panel-body dslist2']/ul/li/a/@href"
            for category in html.xpath(search):
                self.category_urls.append(self.OPINIONS_BASE + category)
            
    def get_opinions_from_categories(self):
        for category_url in self.category_urls:
            category = category_url.split('/')[-2]
            request = self.get_url(category_url)    

            if request.status_code == 200:
                html = lxml.html.fromstring(request.text)
                search = "//table[@class='table table-bordered']/tr"

                for row in html.xpath(search):
                    opinion = []
                    for cell in row.xpath('./td'):
                        opinion.append(cell.text_content())
                        for pdf_path in cell.xpath('./a/@href'):
                            opinion.append(self.BASE + pdf_path)
                            
                    if opinion:
                        # Slip opinions have extra 'reporter' column as first
                        # column. Add blank first column to non slip opinions
                        if len(opinion) == 6:
                            opinion = [''] + opinion

                        # Standardize published date to YYYY-MM-DD format
                        opinion[1] = opinion[1].replace('-', '/')
                        opinion[1] = datetime.strptime(opinion[1], "%m/%d/%y").strftime("%Y-%m-%d")                

                        self.opinions.append(Opinion(
                            category=category,
                            reporter=opinion[0],
                            published=opinion[1],
                            docket=opinion[2],
                            name=opinion[3],
                            pdf_url=opinion[4],
                            justice=Justice(opinion[5]),
                            part=opinion[6],
                            discovered=timezone.now(),
                        ))

    def ingest_new_opinions(self):
        for opinion in self.opinions:
            # If find match on all fields already in database, skip and continue
            if Opinion.objects.filter(
                name=opinion.name,
                pdf_url=opinion.pdf_url,
                published=opinion.published,
                category=opinion.category,
                reporter=opinion.reporter,
                docket=opinion.docket,
                justice=opinion.justice,
                part=opinion.part):

                # Remove previously discovered opinion from processig list
                del self.opinions[self.opinions.index(opinion)]
                continue
            
            # Ingest new opinion to database
            opinion.save()

            # Check if opinion with same name exists. Sometimes SCOTUS fixes and republishes 
            # opinion with same opinion name, but usually a different pdf file name
            opinion.previously_discovered_citations = []
            for previously_discovered in Opinion.objects.get(name=opinion.name):
                previously_discovered.updated = True
                previously_discovered.save()
                opinion.previously_discovered_citations.append(previously_discovered.
   
                # Gather previous opinion's scraped and validated citations
                citations = Citation.objects.filter(opinion=previously_discovered)
                for citation in Citation.objects.filter(opinion=previously_discovered):
                    opinion.previously_discovered_citations.append(citation.scraped)
                    if citation.validated and citation.validated != citation.scraped:
                        opinion.previously_discovered_citations.append(citation.validated)
            
    def ingest_new_citations(self):
        for opinion in self.opinions:
            local_pdf = settings.PDF_DIR + opinion.id + '.pdf'
            opinion.pdf = Pdf(
                opinion.pdf_url,
                local_pdf,
            )
            opinion.pdf.download()
            opinion.pdf.scrape_urls()

            for url in opinion.pdf.urls:
                # Skip citation if ingested in previous discovery
                if url in opinion.previously_discovered_citations:
                    continue
            
                # Check urls status, and see if archived
                status = self.check_url_status(url)

                new_citation = Citation(
                    opinion=Opinion(opinion.id),
                    scraped=url,
                    rotted=status['rotted'],
                    redirected=status['redirected'],
                    archived_lc=status['archived_lc'],
                    archivedis=status['archived_ia'],
                )
                new_citation.save()

    def check_url_status(self, url):
        status = {
            'rotted': False,
            'redirected': False,
            'archived_lc': False,
            'archived_ia': False,
        }

        request = self.get_url(url)
        if request.status_code == 404:
            status['rotted'] = True
        elif request.status_code in [302, 301]:
            status['redirected'] = True

        request = self.get_url(Citation.WAYBACKS['lc'] + url)
        if request.status_code == 200:
            status['archived_lc'] = True

        request = self.get_url(Citation.WAYBACKS['ia'] + url)
        if request.status_code == 200:
            status['archived_ia'] = True

        return status

