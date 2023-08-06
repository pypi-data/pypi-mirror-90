from __future__ import unicode_literals
from __future__ import absolute_import
from setuptools import setup, find_packages
from io import open

__version__ = 'undefined'

exec(open('forgepastebin/version.py').read())

setup(name='ForgePastebin',
      version=__version__,
      description="Pastebin plugin for the Apache Allura platform",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tim Van Steenburgh',
      author_email='tvansteenburgh@geek.net',
      url='http://sf.net/p/forgepastebin',
      license='Apache 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
      ],
      scripts=[
        ],
      entry_points="""
      # -*- Entry points: -*-
      [allura]
      Pastebin=forgepastebin.app:ForgePastebin
      """,
      )
