#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://AI_UI.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='AI_UI',
    version='0.1.0',
    description='GUI for Absolute Integrator',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Absolute Integrator Development Team',
    author_email='lewysbjones@gmail.com',
    url='https://github.com/AbsoluteIntegrator/AI_UI',
    packages=[
        'AI_UI',
    ],
    package_dir={'AI_UI': 'AI_UI'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='AI_UI',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)