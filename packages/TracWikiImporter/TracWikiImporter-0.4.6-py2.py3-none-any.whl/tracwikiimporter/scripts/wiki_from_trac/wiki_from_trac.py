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
import argparse
import logging
from tempfile import NamedTemporaryFile
from tg.decorators import cached_property

from tracwikiimporter.scripts.wiki_from_trac.extractors import WikiExporter
from tracwikiimporter.scripts.wiki_from_trac.loaders import load_data

from allura.scripts import ScriptTask


log = logging.getLogger(__name__)


class WikiFromTrac(ScriptTask):
    """Import Trac Wiki to Allura Wiki"""
    @classmethod
    def parser(cls):
        parser = argparse.ArgumentParser(description='Import wiki from '
            'Trac to allura wiki')

        parser.add_argument('trac_url', type=str, help='Trac URL')
        parser.add_argument('-t', '--token', dest='token',
                            help='OAuth bearer token (generate at /auth/oauth/)')
        parser.add_argument('-p', '--project', dest='project', help='Project to import to')
        parser.add_argument('-n', '--neighborhood', dest='neighborhood', help="URL prefix of destination neighborhood (e.g. 'p')", default='p')
        parser.add_argument('-f', '--forum', dest='forum', help='Forum tool to import to')
        parser.add_argument('-w', '--wiki', dest='wiki', help='Wiki tool to import to')
        parser.add_argument('-u', '--base-url', dest='base_url', default='https://sourceforge.net', help='Base Allura (%(default)s for default)')
        parser.add_argument('-o', dest='import_opts', default=[], action='append', help='Specify import option(s)', metavar='opt=val')
        parser.add_argument('--user-map', dest='user_map_file', help='Map original users to SF.net users', metavar='JSON_FILE')
        parser.add_argument('--validate', dest='validate', action='store_true', help='Validate import data')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose operation')
        parser.add_argument('-c', '--continue', dest='cont', action='store_true', help='Continue import into existing tracker')
        parser.add_argument('-C', '--converter', dest='converter',
                            default='html2text',
                            help='Converter to use on wiki text. '
                                 'Available options: '
                                 'html2text (default) or regex')

        return parser

    @classmethod
    def execute(cls, options):
        options.neighborhood = options.neighborhood.strip('/')
        with NamedTemporaryFile('w+') as f:
            WikiExporter(options.trac_url, options).export(f)
            f.flush()
            load_data(f.name, cls.parser(), options)


if __name__ == '__main__':
    WikiFromTrac.main()
