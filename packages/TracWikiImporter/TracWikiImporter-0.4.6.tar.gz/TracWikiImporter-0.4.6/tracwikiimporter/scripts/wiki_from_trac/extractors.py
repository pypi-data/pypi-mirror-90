#       Licensed to the Apache Software Foundation (ASF) under one
#       or more contributor license agreements.  See the NOTICE file
#       distributed with this work for additional information
#       regarding copyright ownership.  The ASF licenses this file
#       to you under the Apache License, Version 2.0 (the
#       "License"); you may not use this file except in compliance
#       with the License.  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#       Unless required by applicable law or agreed to in writing,
#       software distributed under the License is distributed on an
#       "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#       KIND, either express or implied.  See the License for the
#       specific language governing permissions and limitations
#       under the License.

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
import logging
import re
import sys
import json
import traceback
from six.moves.urllib.parse import quote, unquote
from six.moves.urllib.parse import urljoin, urlsplit
from six.moves.html_parser import HTMLParser

from forgeimporters.base import ProjectExtractor
from forgeimporters.trac import TracURLValidator
import six
urlopen = ProjectExtractor.urlopen

import html2text

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class WikiExporter(object):

    PAGE_LIST_URL = 'wiki/TitleIndex'
    PAGE_URL = 'wiki/%s'
    CONTENT_DIV_ATTRS = {'class': 'wikipage searchable'}
    EXCLUDE_PAGES = [
        'CamelCase',
        'InterMapTxt',
        'InterTrac',
        'InterWiki',
        'PageTemplates',
        'SandBox',
        'TitleIndex',
        'TracAccessibility',
        'TracAdmin',
        'TracBackup',
        'TracBrowser',
        'TracChangeset',
        'TracEnvironment',
        'TracFineGrainedPermissions',
        'TracGuide',
        'TracImport',
        'TracIni',
        'TracInterfaceCustomization',
        'TracLinks',
        'TracLogging',
        'TracNavigation',
        'TracNotification',
        'TracPermissions',
        'TracPlugins',
        'TracQuery',
        'TracReports',
        'TracRevisionLog',
        'TracRoadmap',
        'TracRss',
        'TracSearch',
        'TracSupport',
        'TracSyntaxColoring',
        'TracTickets',
        'TracTicketsCustomFields',
        'TracTimeline',
        'TracUnicode',
        'TracWiki',
        'TracWorkflow',
        'WikiDeletePage',
        'WikiFormatting',
        'WikiHtml',
        'WikiMacros',
        'WikiNewPage',
        'WikiPageNames',
        'WikiProcessors',
        'WikiRestructuredText',
        'WikiRestructuredTextLinks',
        'RecentChanges',
    ]
    RENAME_PAGES = {
        'WikiStart': 'Home',  # Change the start page name to Home
        'Home': 'WikiStart',  # Rename the Home page to WikiStart
    }

    def __init__(self, base_url, options):
        self.base_url = TracURLValidator().to_python(base_url)
        self.options = options

    def export(self, out):
        pages = []
        for title in self.page_list():
            try:
                pages.append(self.get_page(title))
            except:
                self.log('Cannot fetch page %s. Skipping' % title)
                self.log(traceback.format_exc())
                continue
        out.write(json.dumps(pages, indent=2, sort_keys=True))
        out.write('\n')

    def log(self, msg):
        log.info(msg)
        if self.options.verbose:
            print(msg, file=sys.stderr)

    def url(self, suburl, type=None):
        url = urljoin(self.base_url, suburl)
        if type is None:
            return url
        glue = '&' if '?' in suburl else '?'
        return  url + glue + 'format=' + type

    def fetch(self, url):
        return urlopen(url)

    def page_list(self):
        url = urljoin(self.base_url, self.PAGE_LIST_URL)
        self.log('Fetching list of pages from %s' % url)
        r = self.fetch(url)
        html = BeautifulSoup(r)
        pages = html.find('div', attrs=self.CONTENT_DIV_ATTRS) \
                    .find('ul').findAll('li')
        decoder = HTMLParser()
        pages = [decoder.unescape(page.find('a').text)
                 for page in pages
                 if page.find('a')
                 and page.find('a').text not in self.EXCLUDE_PAGES]
        # Remove duplicate entries by converting page list to a set.
        # As we're going to fetch all listed pages,
        # it's safe to destroy the original order of pages.
        return set(pages)

    def get_page(self, title):
        title = quote(title)
        convert_method = '_get_page_' + self.options.converter
        content = getattr(self, convert_method)(title)
        page = {
            'title': self.convert_title(title),
            'text': self.convert_content(content),
            'labels': '',
        }
        return page

    def _get_page_html2text(self, title):
        url = self.url(self.PAGE_URL % title)
        self.log('Fetching page %s' % url)
        r = self.fetch(url)
        html = BeautifulSoup(r)
        return html.find('div', attrs=self.CONTENT_DIV_ATTRS)

    def _get_page_regex(self, title):
        url = self.url(self.PAGE_URL % title, 'txt')
        self.log('Fetching page %s' % url)
        r = self.fetch(url)
        return r

    def convert_title(self, title):
        title = self.RENAME_PAGES.get(title, title)
        title = title.replace('/', '-')  # Handle subpages
        title = title.rstrip('?')  # Links to non-existent pages ends with '?'
        return title

    def convert_content(self, content):
        convert_method = '_convert_content_' + self.options.converter
        return getattr(self, convert_method)(content)

    def _convert_wiki_toc_to_markdown(self, content):
        """
        Removes contents of div.wiki-toc elements and replaces them with
        the '[TOC]' markdown macro.
        """
        for toc in content('div', attrs={'class': 'wiki-toc'}):
            toc.string = '[TOC]'
        return content

    def _convert_content_html2text(self, content):
        html2text.BODY_WIDTH = 0  # Don't wrap lines
        content = self._convert_wiki_toc_to_markdown(content)
        content = html2text.html2text(six.text_type(content))
        # Convert internal links
        internal_url = urlsplit(self.base_url).path + 'wiki/'
        internal_link_re = r'\[([^]]+)\]\(%s([^)]*)\)' % internal_url
        internal_link = re.compile(internal_link_re, re.UNICODE)
        def sub(match):
            caption = match.group(1)
            page = self.convert_title(match.group(2))
            if caption == page:
                link = '[%s]' % unquote(page)
            else:
                link = '[%s](%s)' % (caption, page)
            return link
        return internal_link.sub(sub, content)

    def _convert_content_regex(self, text):
        # https://gist.github.com/sgk/1286682
        text = re.sub('\r\n', '\n', text)
        text = re.sub(r'{{{(.*?)}}}', r'`\1`', text)

        def indent4(m):
            return '\n    ' + m.group(1).replace('\n', '\n    ')

        text = re.sub(r'(?sm){{{\n(.*?)\n}}}', indent4, text)
        text = re.sub(r'(?m)^====\s+(.*?)\s+====$', r'#### \1', text)
        text = re.sub(r'(?m)^===\s+(.*?)\s+===$', r'### \1', text)
        text = re.sub(r'(?m)^==\s+(.*?)\s+==$', r'## \1', text)
        text = re.sub(r'(?m)^=\s+(.*?)\s+=$', r'# \1', text)
        text = re.sub(r'^       * ', r'****', text)
        text = re.sub(r'^     * ', r'***', text)
        text = re.sub(r'^   * ', r'**', text)
        text = re.sub(r'^ * ', r'*', text)
        text = re.sub(r'^ \d+. ', r'1.', text)
        a = []
        for line in text.split('\n'):
            if not line.startswith('    '):
                line = re.sub(r'\[(https?://[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](\1)', line)
                line = re.sub(r'\[(wiki:[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](/\1/)', line)
                line = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'\1', line)
                line = re.sub(r'\'\'\'(.*?)\'\'\'', r'*\1*', line)
                line = re.sub(r'\'\'(.*?)\'\'', r'_\1_', line)
            a.append(line)
        return '\n'.join(a)
