#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(name='semences05',
      version='0.1',
      description='Application web pour le partage de semence dans les Hautes-Alpes',
      author='Swan Mougnoz',
      author_email='mougnoz.swan@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          '': ['*.ini', '*.html', '*.js', '*.css', '*.jpg', '*.png']
      },
)


