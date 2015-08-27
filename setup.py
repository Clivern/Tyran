from setuptools import setup

from pyarchiver import __VERSION__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyarchiver",
    version = __VERSION__,
    author = "Clivern",
    author_email = "support@clivern.com",
    description="Python Compression and Archiving Library",
    license = "MIT",
    keywords = "compression,archiving,tarfile,zipfile",
    url="http://clivern.com/portfolio/pyarchiver",
    packages=['pyarchiver'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)