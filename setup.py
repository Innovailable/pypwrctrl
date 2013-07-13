#!/usr/bin/env python3

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pypwrctrl",
    version = "0.1.2",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("Anel NET-PwrCtrl library and command line utility"),
    license = "GPLv3",
    keywords = "net-pwrctrl anel",
    url = "https://github.com/thammi/pypwrctrl",
    packages=['pypwrctrl'],
    long_description=read('README.md'),
    # TODO: extend ...
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Home Automation",
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            'pypwrctrl = pypwrctrl.main:main',
            ],
        },
)

