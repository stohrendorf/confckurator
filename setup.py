#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

setup(name='Confckurator',
      version='1.0',
      description='Don\'t f*ck with configs anymore',
      author='Steffen Ohrendorf',
      author_email='steffen.ohrendorf@gmx.de',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      zip_safe=False,
      install_requires=['werkzeug', 'flask', 'flask-restful', 'sqlalchemy'],
      include_package_data=True
      )
