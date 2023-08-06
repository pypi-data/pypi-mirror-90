from __future__ import unicode_literals
from __future__ import absolute_import
from unittest import TestCase
from mock import Mock, patch
from ming.odm import ThreadLocalORMSession

from allura.tests import TestController
from allura.tests.decorators import with_wiki
from allura import model as M

from tracwikiimporter.importer import (
    TracWikiImporter,
    TracWikiImportController,
    )
from tracwikiimporter.scripts.wiki_from_trac.extractors import WikiExporter


class TestTracWikiImporter(TestCase):

    @patch('tracwikiimporter.importer.AuditLog')
    @patch('tracwikiimporter.importer.session')
    @patch('tracwikiimporter.importer.tempfile.NamedTemporaryFile')
    @patch('tracwikiimporter.importer.g')
    @patch('tracwikiimporter.importer.WikiFromTrac')
    @patch('tracwikiimporter.importer.load_data')
    @patch('tracwikiimporter.importer.argparse.Namespace')
    @patch('tracwikiimporter.importer.WikiExporter')
    def test_import_tool(self, WikiExporter, Namespace, load_data,
            WikiFromTrac, g, NamedTemporaryFile, session, AuditLog):
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        export_file = NamedTemporaryFile.return_value.__enter__.return_value
        export_file.name = '/my/file'

        importer = TracWikiImporter()
        importer.get_token = Mock()
        app = Mock(name='ForgeWikiApp')
        app.config.options.mount_point = 'pages'
        app.url = 'foo'
        project = Mock(name='Project', shortname='myproject')
        project.install_app.return_value = app
        project.url.return_value = '/nbhd/foobar/subproj/'
        user = Mock(name='User', _id='id')
        res = importer.import_tool(project, user,
                mount_point='pages',
                mount_label='Pages',
                trac_url='http://example.com/trac/url')
        self.assertEqual(res, app)
        project.install_app.assert_called_once_with(
                'Wiki', mount_point='pages', mount_label='Pages',
                import_id={
                        'source': 'Trac',
                        'trac_url': 'http://example.com/trac/url',
                    },
            )
        importer.get_token.assert_called_once_with(user)
        WikiExporter.assert_called_once_with('http://example.com/trac/url',
                Namespace.return_value)
        WikiExporter.return_value.export.assert_called_once_with(export_file)
        load_data.assert_called_once_with('/my/file',
                WikiFromTrac.parser.return_value, Namespace.return_value)
        AuditLog.log.assert_called_once_with(
                'import tool pages from http://example.com/trac/url',
                project=project,
                user=user,
                url='foo',
            )
        g.post_event.assert_called_once_with('project_updated')

    @patch('tracwikiimporter.importer.session')
    @patch('tracwikiimporter.importer.h')
    def test_import_tool_failure(self, h, session):
        importer = TracWikiImporter()
        importer.get_token = Mock(side_effect=ValueError)
        app = Mock(name='ForgeWikiApp')
        project = Mock(name='Project', shortname='myproject')
        project.install_app.return_value = app
        user = Mock(name='User', _id='id')
        self.assertRaises(ValueError, importer.import_tool,
                project, user,
                mount_point='pages',
                mount_label='Pages',
                trac_url='http://example.com/trac/url')
        h.make_app_admin_only.assert_called_once_with(app)


class TestTracWikiImportController(TestController, TestCase):
    def setUp(self):
        """Mount Trac import controller on the Wiki admin controller"""
        super(self.__class__, self).setUp()
        from forgewiki.wiki_main import WikiAdminController
        WikiAdminController._importer = \
                TracWikiImportController(TracWikiImporter())

    @with_wiki
    def test_index(self):
        r = self.app.get('/p/test/admin/wiki/_importer/')
        self.assertIsNotNone(r.html.find(attrs=dict(name="trac_url")))
        self.assertIsNotNone(r.html.find(attrs=dict(name="mount_label")))
        self.assertIsNotNone(r.html.find(attrs=dict(name="mount_point")))

    @with_wiki
    @patch('forgeimporters.trac.requests.head')
    @patch('forgeimporters.base.import_tool')
    def test_create(self, import_tool, head):
        head.return_value.status_code = 200
        params = dict(
            trac_url='http://example.com/trac/url',
            mount_label='mylabel',
            mount_point='mymount',
        )
        r = self.app.post('/p/test/admin/wiki/_importer/create', params,
                          status=302)
        self.assertEqual(r.location, 'http://localhost/p/test/admin/')
        self.assertEqual('mymount',
                         import_tool.post.call_args[1]['mount_point'])
        self.assertEqual('mylabel',
                         import_tool.post.call_args[1]['mount_label'])
        self.assertEqual('http://example.com/trac/url/',
                         import_tool.post.call_args[1]['trac_url'])

    @with_wiki
    @patch('forgeimporters.trac.requests.head')
    @patch('forgeimporters.base.import_tool')
    def test_create_limit(self, import_tool, head):
        head.return_value.status_code = 200
        project = M.Project.query.get(shortname='test')
        project.set_tool_data('TracWikiImporter', pending=1)
        ThreadLocalORMSession.flush_all()
        params = dict(
            trac_url='http://example.com/trac/url',
            mount_label='mylabel',
            mount_point='mymount',
        )
        r = self.app.post('/p/test/admin/wiki/_importer/create', params,
                          status=302).follow()
        self.assertIn('Please wait and try again', r)
        self.assertEqual(import_tool.post.call_count, 0)

    @with_wiki
    @patch('forgeimporters.trac.requests.head')
    @patch('forgeimporters.base.import_tool')
    def test_created_not_found(self, import_tool, head):
        head.return_value.status_code = 404
        params = dict(
            trac_url='http://example.com/trac/url',
            mount_label='mylabel',
            mount_point='mymount',
        )
        r = self.app.post('/p/test/admin/wiki/_importer/create', params)
        self.assertEqual(import_tool.post.call_count, 0)


class TestWikiExporter(TestCase):

    @patch('forgeimporters.trac.requests')
    def test_url_canonicalization(self, requests):
        requests.head.return_value.status_code = 200
        test_urls = [
            'https://sourceforge.net/apps/trac/shareaza',
            'https://sourceforge.net/apps/trac/shareaza/',
            'https://sourceforge.net/apps/trac/shareaza/wiki',
            'https://sourceforge.net/apps/trac/shareaza/wiki/',
            'https://sourceforge.net/apps/trac/shareaza/wiki/SomePage',
        ]
        for url in test_urls:
            self.assertEqual(WikiExporter(url, None).base_url,
                             'https://sourceforge.net/apps/trac/shareaza/')
        self.assertEqual(WikiExporter('http://foo.com/wiki/bar/', None).base_url,
                         'http://foo.com/wiki/bar/')

    def test_page_list__special_chars(self):
        class WikiExporterFunnyPages(WikiExporter):
            def __init__(self, base_url, options):
                self.base_url = base_url
                self.options = options

            def fetch(self, url):
                return '''
                    <div class="wikipage searchable">
                        <ul>
                            <li><a>Hello World</a></li>
                            <li><a>Foo &amp; Bar</a></li>
                        </ul>
                    </div>
                    '''

        exp = WikiExporterFunnyPages('http://example.com/trac/', Mock())
        self.assertEqual(exp.page_list(), {'Hello World', 'Foo & Bar'})
