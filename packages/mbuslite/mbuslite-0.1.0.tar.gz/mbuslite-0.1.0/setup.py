
from pathlib import Path
from setuptools import setup
import sys

here = Path( __file__ ).parent.resolve()
sys.path.insert( 0, here )

import mbuslite



setup(
    name = mbuslite.__title__,
    version = '0.0.0' if mbuslite.__version__ == 'git' else mbuslite.__version__,
    description = mbuslite.__description__,
    long_description = ( here / 'README.rst' ).read_text( encoding = 'utf-8' ),
    long_description_content_type = 'text/x-rst',
    url = mbuslite.__url__,
    author = mbuslite.__author__,
    author_email = mbuslite.__author_email__,
    license = mbuslite.__license__,
    packages = [ 'mbuslite' ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)

