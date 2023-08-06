# -*- coding: utf-8 -*-

from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='pymbtc',
        version='0.21',
        description='API (dados e negociação) do Mercado Bitcoin',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='http://github.com/lbltavares/pymbtc',
        author='lbltavares',
        license='MIT',
        packages=['pymbtc'],
        zip_safe=False
    )