#!/usr/bin/env python
import codecs
import re
import sys
import pydns
import os
from setuptools import setup


if not os.path.exists('README.md') and 'sdist' in sys.argv:
    with codecs.open('README.rst', encoding='utf8') as f:
        rst = f.read()
    code_block = '(:\n\n)?\.\. code-block::.*'
    rst = re.sub(code_block, '::', rst)
    with codecs.open('README.md', encoding='utf8', mode='wb') as f:
        f.write(rst)


try:
    readme = 'README.md' if os.path.exists('README.md') else 'README.rst'
    long_description = codecs.open(readme, encoding='utf-8').read()
except:
    long_description = 'Could not read README.md'


setup(
    name = 'pydns',
    version = pydns.__version__,
    description = 'Python Wrapper around the PowerDNS REST API',
    author = 'Vinzenz Stadtmueller',
    author_email = 'info@edgelab.de',
    license = "Apache 2.0",
    url = 'https://github.com/edgelab-pw/pypdns',
    download_url = 'http://pypi.python.org/pypi/pypdns',
    keywords = ['pdns', 'powerdns', 'api'],
    packages=['pydns'],
    classifiers = [ #http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires=[
        "requests >= 2.9.1",
    ],
    long_description = long_description
)