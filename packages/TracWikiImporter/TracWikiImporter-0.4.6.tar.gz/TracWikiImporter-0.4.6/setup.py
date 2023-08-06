from __future__ import unicode_literals
from __future__ import absolute_import
from setuptools import setup, find_packages

__version__ = '0.4.6'

setup(name='TracWikiImporter',
      version=__version__,
      description="Trac Wiki Importer plugin for the Allura platform",
      long_description="",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tim Van Steenburgh',
      author_email='tvansteenburgh@gmail.com',
      url='http://sf.net/p/tracwikiimporter',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=['html2text'],
      entry_points="""
      # -*- Entry points: -*-
      [allura.importers]
      trac-wiki = tracwikiimporter.importer:TracWikiImporter
      """,
      )
