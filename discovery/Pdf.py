# -*- coding: utf-8 -*-

import re
import io
import os

#duplicate imports?
from requests import get
from django.utils import timezone
from scotus import settings

from datetime import datetime
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter


class Pdf:
    def __init__(self, url=False, local_file=False):
        self.url = url
        self.local_file = local_file
        self.urls = []

    def download(self):
        if not self.url or not self.local_file:
            return False

        request = get(self.url, headers=settings.REQ_HEADER)
        if request.status_code != 200:
            return False

        with open(self.local_file, 'w') as local:
            #ADDRESS: need .decode('utf8') below?
            local.write(request.content) 
            local.close()
 
        return True

    def scrape_urls(self):
        self.extract_text()
        self.extract_urls_from_text()

    def extract_text(self):
        pdf_data = file(self.local_file, 'rb').read()
        pdf_stream = io.BytesIO(pdf_data)
        laparams = LAParams()
        resource_manager = PDFResourceManager(caching=True)
        output_type = 'text'
        codec = 'utf-8'
        output_stream = io.BytesIO()
        pagenos = set()

        device = TextConverter(
            resource_manager,
            output_stream,
            codec=codec,
            laparams=laparams,
        )

        interpreter = PDFPageInterpreter(
            resource_manager,
            device,
        )

        pages = PDFPage.get_pages(
            pdf_stream,
            pagenos,
            maxpages=0,
            caching=True,
            check_extractable=True,
        )

        for page in pages:
            interpreter.process_page(page)

        self.text = output_stream.getvalue().decode('utf8')

    def extract_urls_from_text(self):
        if not self.text:
            return False

        # Replace newlines with spaces, then create newlines at instances of 'http'
        text = re.sub('\n', '', self.text)
        text = re.sub('http', '\nhttp', text)
        lines = text.split('\n')

        # Loop over newlines created, url should be first element
        for line in lines:
            if line.startswith('http'):
                self.urls.append(line.split(' ')[0])
