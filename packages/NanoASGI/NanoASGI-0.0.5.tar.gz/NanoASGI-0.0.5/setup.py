#!/usr/bin/env python

import sys
from setuptools import setup
from os.path import abspath, dirname, join as pathjoin
if sys.version_info < (3, 6):
    raise NotImplementedError("Sorry, you need at least Python 3.6 to use nanoasgi.")

import nanoasgi

here=dir_path = dirname(abspath(__file__))
long_description = open(pathjoin(here, 'README.md')).read()

setup(name='NanoASGI',
      version=nanoasgi.__version__,
      description='Fast and simple ASGI-framework for small web-applications.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author=nanoasgi.__author__,
      author_email='kavindusanthusa@gmail.com',
      url='https://nanoasgi.github.io/NanoASGI',
      py_modules=['nanoasgi'],
      scripts=['nanoasgi.py'],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
    keywords='python, asgi, rest, web-framework, fast, simple, lightweight, micro',
    project_urls={
        'Bug Reports': 'https://github.com/nanoasgi/NanoASGI/issues',
        'Funding': 'https://www.buymeacoffee.com/Ksengine',
        'Say Thanks!': 'https://saythanks.io/to/kavindusanthusa%40gmail.com',
        'Source': 'https://github.com/nanoasgi/NanoASGI',
    }
      )
