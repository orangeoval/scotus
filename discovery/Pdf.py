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
        #ADDRESS: find pythonic way of doing replacement on multiple needle/search terms for all newlines
        #ADDRESS: should be using r'' string format?
        new_lines = ['\n', '&#xD', '\r']
        text = re.sub('\n', '', self.text)
        text = re.sub('http', '\nhttp', text)
        lines = text.split('\n')

        # Loop over newlines created, url should be first element
        for line in lines:
            if line.startswith('http'):

                # Many of the cited urls have poor formatting, such as spaces
                # before and after slashes, spaces after http://, punctuation
                # at the end of the string, etc.  We clean that up here. The
                # weirdness is so inconsistent that we can't systematically
                # fix everything at the moment, which is why a user must verify
                # all scraped links
                common_endings = [
                    'com',
                    'gov',
                    'net',
                    'edu',
                    'mil',
                    'htm',
                    'tml',
                    'php',
                    'asp',
                    'pdf',
                ]
                punctuation = [
                    '.',
                    ',', 
                    ';',
                    '?',
                    '=',
                    ':',
                    '_',
                    '-',
                    '#',
                    '$',
                    '%',
                    '+',
                ]
                partials = [
                    'www', 'www.',
                    'http', 'https',
                    'http:', 'https:',
                    'http:/', 'https:/',
                    'http://', 'https://',
                    'http://www', 'https://www',
                    'http://www.', 'https://www.',
                ]

                words = line.split()
                url = words[0].strip()
                next_word = 1

                # Unnecessary space in url?
                while len(words) >= next_word and \
                    url in partials or \
                    url[-1] == '_' or \
                    (words[next_word][0] and words[next_word][0] in ['/', '_']) or \
                    (len(words[next_word]) >= 3 and url.endswith('.') and words[next_word][0:3] in common_endings):

                    url = url + words[next_word].strip()
                    next_word += 1

                # Punctuation at end of string?
                if url[-1] in punctuation and \
                    words[next_word][0:3] not in common_endings:
                    url = url[0:-1]

                # Some opinions cite the same link multiple times. Add if not
                # already in list
                if not url in self.urls:
                    self.urls.append(url)
