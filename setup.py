# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='yaml-checker',
    version='0.0.1',
    description='Retrieve items from the yaml file. Validate presence of files and directories with varying strictness.',
    long_description=readme,
    author='Katie Doroschak',
    author_email='k.doroschak@gmail.com',
    url='https://github.com/kdoroschak/yaml-checker',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
