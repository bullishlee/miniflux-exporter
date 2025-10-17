#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Miniflux Exporter.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='miniflux-exporter',
    version='1.0.0',
    author='Miniflux Exporter Contributors',
    author_email='',
    description='Export your Miniflux articles to Markdown format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bullishlee/miniflux-exporter',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'examples']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'pylint>=2.12.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'miniflux-export=miniflux_exporter.cli:main',
        ],
    },
    keywords=[
        'miniflux',
        'rss',
        'feed',
        'export',
        'markdown',
        'backup',
        'archiver',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/bullishlee/miniflux-exporter/issues',
        'Source': 'https://github.com/bullishlee/miniflux-exporter',
        'Documentation': 'https://github.com/bullishlee/miniflux-exporter/blob/main/README.md',
    },
    include_package_data=True,
    zip_safe=False,
)
