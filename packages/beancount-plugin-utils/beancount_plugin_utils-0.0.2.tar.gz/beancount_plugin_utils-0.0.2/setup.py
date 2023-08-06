#!/usr/bin/env python3

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='beancount_plugin_utils',
    version='0.0.2',
    description='Plugin for Beancount to share expenses.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Akuukis',
    author_email='akuukis@kalvis.lv',
    download_url='https://pypi.python.org/pypi/beancount_plugin_utils',
    license='GNU AGPLv3',
    package_data={'beancount_plugin_utils': ['../README.md']},
    package_dir={'beancount_plugin_utils': 'beancount_plugin_utils'},
    packages=['beancount_plugin_utils'],
    requires=['beancount (>2.0)'],
    url='https://github.com/Akuukis/beancount_plugin_utils',
)
