#!/usr/bin/env python
from setuptools import setup, find_packages
import codecs

setup(name='aiautomation',
      version='0.3',
      url='',
      license='MIT',
      author='Marvin Ren',
      author_email='dtrex@163.com',
      description='The Automation Test Framework',
      packages=find_packages(exclude=['tests']),
      long_description=codecs.open('README.md', 'r', 'utf-8').read(),
      zip_safe=False,
      setup_requires=['nose>=1.0', 'selenium>=3.8.1'],
      test_suite='nose.collector')