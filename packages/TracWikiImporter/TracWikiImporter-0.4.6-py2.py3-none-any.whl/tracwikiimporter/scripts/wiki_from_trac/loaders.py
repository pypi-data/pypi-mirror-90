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
import json
import logging

from allura.lib.import_api import AlluraImportApiClient
import six
from io import open


log = logging.getLogger(__name__)

def load_data(doc_file_name=None, optparser=None, options=None):
    import_options = {}
    for s in options.import_opts:
        k, v = s.split('=', 1)
        if v == 'false':
            v = False
        import_options[k] = v

    user_map = {}
    if options.user_map_file:
        f = open(options.user_map_file)
        try:
            user_map = json.load(f)
            if type(user_map) is not type({}):
                raise ValueError
            for k, v in six.iteritems(user_map):
                print(k, v)
                if not isinstance(k, six.string_types) or not isinstance(v, six.string_types):
                    raise ValueError
        except ValueError:
            optparser.error('--user-map should specify JSON file with format {"original_user": "sf_user", ...}')
        finally:
            f.close()

    import_options['user_map'] = user_map

    cli = AlluraImportApiClient(options.base_url, options.token, options.verbose)
    doc_txt = open(doc_file_name).read()

    if options.wiki:
        import_wiki(cli, options.project, options.wiki, options, doc_txt)


def import_wiki(cli, project, tool, options, doc_txt):
    url = '/rest/{neighborhood}/{project}/{tool}'.format(
            neighborhood=options.neighborhood,
            project=project,
            tool=tool,
            )
    log.info('Loading trac wiki in to %s', url)
    doc = json.loads(doc_txt)
    if 'wiki' in doc and 'default' in doc['wiki'] and 'artifacts' in doc['wiki']['default']:
        pages = doc['trackers']['default']['artifacts']
    else:
        pages = doc
    if options.verbose:
        print("Processing %d pages" % len(pages))
    for page in pages:
        title = six.ensure_text(page.pop('title'))
        r = cli.call(url + '/' + title, **page)
        assert r == {}
        print('Imported wiki page %s' % title)
