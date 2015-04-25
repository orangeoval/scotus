from scotus import settings
from django.db import models
from opinions.models import Opinion
from citations.models import Citation
from requests import get
from datetime import datetime
import lxml.html

class Discovery:
    def __init__(self):
        self.BASE = 'http://www.supremecourt.gov'
        self.OPINIONS_BASE = self.BASE + '/opinions/'
        self.OPINIONS_MAIN_PAGE = self.OPINIONS_BASE + 'opinions.aspx'
        self.category_urls = []
        self.opinions = []

    def run(self):
        self.get_opinion_category_urls()
        self.get_opinions_from_categories()

    def get_opinion_category_urls(self):
        request = get(self.OPINIONS_MAIN_PAGE, headers=settings.REQ_HEADER)

        if request.status_code == 200:
            html = lxml.html.fromstring(request.text)
            search = "//div[@class='panel-body dslist2']/ul/li/a/@href"
            for category in html.xpath(search):
                self.category_urls.append(self.OPINIONS_BASE + category)
            
    def get_opinions_from_categories(self):
        for category_url in self.category_urls:
            category = category_url.split('/')[-2]
           
            request = get(category_url, headers=settings.REQ_HEADER)    
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

                        # Slip opinions have extra 'reporter' as first column
                        # add blank first column to non slip opinions
                        if len(opinion) == 6:
                            opinion = [''] + opinion

                        # Standardize published date from American mm/dd/yy
                        # or mm-dd-yy format
                        opinion[1] = opinion[1].replace('-', '/')
                        opinion[1] = datetime.strptime(opinion[1], "%m/%d/%y").strftime("%Y-%m-%d")                
                        self.opinions.append({
                            'category': category,
                            'reporter': opinion[0],
                            'published': opinion[1],
                            'docket': opinion[2],
                            'name': opinion[3],
                            'pdf_url': opinion[4],
                            'justice': opinion[5],
                            'part': opinion[6],
                        })

    def scrape_urls_from_pdf(self):
        pass
