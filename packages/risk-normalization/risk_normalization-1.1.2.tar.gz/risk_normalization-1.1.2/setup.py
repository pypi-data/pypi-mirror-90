#  setup.py
#    for risk_normalization.py package
#  Modified Monday, January 4, 2021

import os
import setuptools
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = 'risk_normalization',
    version = '1.1.2',
    author = 'Dr. Howard Bandy',
    author_email = 'howard@blueowlpress.com',
    description = 'Compute safe_f and CAR25 for a list of trades',
    long_description_content_type='text/markdown',
    long_description = long_description,
    url='https://github.com/howardbandy/risk_normalization/blob/master/risk_normalization.py',
    packages=setuptools.find_packages(include=['risk_normalization']),
    license = 'MIT',
    install_requires=[],
    python_requires='>=3.6',
)
