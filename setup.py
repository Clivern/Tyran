"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""

from setuptools import setup
from pyarchiver import __VERSION__
import os

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyarchiver",
    version = __VERSION__,
    author = "Clivern",
    author_email = "hello@clivern.com",
    description="Python Compression and Archiving Library",
    license = "MIT",
    keywords = "compression,archiving,tarfile,zipfile",
    url = "http://clivern.github.io/PyArchiver/",
    packages = ['pyarchiver'],
    long_description = read('README.md'),
    classifiers = [
        'Classifier: Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        # Support Python-2.x and Python-3.x
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)