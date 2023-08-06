#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='rwth_nb',
      description='RWTH Python Library for Jupyter Notebooks',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.rwth-aachen.de/jupyter/rwth-nb',
      author='Christian Rohlfing, Lars Thieling, Christoph Weyer, Jens Schneider, Steffen Vogel',
      author_email='rohlfing@ient.rwth-aachen.de',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[], # todo
      use_scm_version=True,
      setup_requires=[
          'setuptools_scm'
      ],
      zip_safe=False)
