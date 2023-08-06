import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "slxvfs",
    version = "0.0.1",
    author = "Sx",
    author_email = "orencape@gmail.com",
    description = ('SLX - '),
    license = None,
    keywords = ["slx", "slm", "slf", "generator", "giftcard generator"],
    url = "http://packages.python.org/slxvfs",
    long_description=read('README.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
