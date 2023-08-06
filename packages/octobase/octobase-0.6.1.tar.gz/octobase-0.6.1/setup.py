#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name            = 'octobase',
    version         = '0.6.1',
    author          = 'Octoboxy',
    author_email    = 'office@octoboxy.com',
    description     = 'The First Building Block For Any Python Project',
    url             = 'https://bitbucket.org/octoboxy/octobase/',
    python_requires = '>=3.6',
    classifiers     = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
    ],
    packages        = setuptools.find_packages(),
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
)
