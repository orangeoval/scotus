from django.db import models
from HTMLParser import HTMLParser
from requests import get

class SCOTUSParser(HTMLParser):
    def __init__(self):
        self.in_pannel = False
        self.in_opinion_table = False
        self.in_table_row = False
        self.table_data = []
        self.row_data = []
        self.category_paths = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        attrs = dict((k, v) for k, v in attrs)
        if tag == 'div' and 'class' in attrs:
            if attrs['class'] == 'panel-body dslist2':
                self.in_pannel = True
        if tag == 'table' and 'class' in attrs:
            if attrs['class'] == 'table table-bordered':
                self.in_opinion_table = True
        if tag == 'tr' and self.in_opinion_table:
            self.in_table_row = True
        if tag == 'a' and 'href' in attrs:
            if self.in_table_row:
                self.row_data.append(attrs['href'])
            elif self.in_pannel:
                self.category_paths.append(attrs['href'])
    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_pannel = False
        if tag == 'table':
            self.in_opinion_table = False;
        if tag == 'tr' and self.row_data:
            self.table_data.append(self.row_data)
            self.row_data = []

    def handle_data(self, data):
        if self.in_table_row:
            if data.strip():
                self.row_data.append(data.strip())

    @classmethod
    def custom_parse(cls, html, return_variable):
        parser = cls()
        parser.feed(html)
        parser.close()
        return getattr(parser, return_variable)

class Discovery:
    def __init__(self):
        self.BASE = 'http://www.supremecourt.gov'
        self.OPINIONS_BASE = self.BASE + '/opinions/'
        self.OPINIONS_MAIN_PAGE = self.OPINIONS_BASE + 'opinions.aspx'
        self.category_urls = []
        self.opinions = []

    def fetch(self):
        request = get(self.OPINIONS_MAIN_PAGE)
        if request.status_code == 200:
  
            # Fetch category urls
            category_paths = SCOTUSParser.custom_parse(
                request.text,
                'category_paths',
            )
            for path in category_paths:
                self.category_urls.append(self.OPINIONS_BASE + path)

            # Fetch opinion urls
            for category in self.category_urls:
                request = get(category)
                if request.status_code == 200:
                    table_data = SCOTUSParser.custom_parse(
                        request.text,
                        'table_data',
                    )

                    # Remove first row, it's the header fields
                    del table_data[0]

                    for row in table_data:
                        self.opinions.append({
                            'reporter': row[0],
                            'published': row[1],
                            'docket': row[2],
                            'pdf_url': self.BASE + row[3],
                            'name': row[4],
                            'justice': row[5],
                            'part': row[6],
                        })

                    for opinion in self.opinions:
                        print "OPINION:", opinion

                    #print "TABLE:", category
                    #for row in table_data:
                    #    print "ROW:"
                    #    for cell in row:
                    #        print "\tCELL:", cell
         
                    #REMOVE
                    import sys
                    sys.exit(0)
