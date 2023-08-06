#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ravand_plotting',

    version='1.0.0',

    description='Plotting package for Backtrader (Bokeh)',

    python_requires='>=3.6',

    author='soroush',
    author_email='soroush_safarii@yahoo.com',

    long_description=long_description,
    long_description_content_type="text/markdown",

    license='GPLv3+',
    url="https://github.com/coci/ravand_plot",
    project_urls={},

    # What does your project relate to?
    keywords=['trading', 'development', 'plotting', 'backtrader'],

    packages=setuptools.find_packages(),
    
    package_data={'backtrader_plotting.bokeh': ['templates/*.j2']},

    install_requires=[
        'backtrader',
        'bokeh~=2.0.0',
        'jinja2',
        'pandas',
        'matplotlib',
        'markdown2',
    ],
)
