#!/usr/bin/env python

import os
import sys

from webinspectapi import __version__ as version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r') as f:
    readme = f.read()

# Publish helper
if sys.argv[-1] == 'install':
    os.system('python3 setup.py sdist --formats=zip')
    sys.exit(0)
    
setup(
    name='webinspectapi',
    packages=['webinspectapi'],
    version=version,
    description='Python library enumerating the WebInspect RESTFul API scan, securebase, and proxy endpoints.',
    long_description=readme,
    author='Brandon Spruth',
    author_email='brandon@fortifyadmin.io',
    url='https://github.com/webbreaker/webinspectapi',
    download_url='https://github.com/webbreaker/webinspectapi/tarball/' + version,
    license='MIT',
    zip_safe=True,
    install_requires=['requests'],
    keywords=['webinspect', 'api', 'security', 'software', 'hpe', 'micro focus', 'dast'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
