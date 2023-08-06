import os
import sys
import json

from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(name='oracle_kernel',
      version='0.1.0',
      description='A oracle kernel for Jupyter.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/Hourout/oracle_kernel',
      author='JinQing Lee',
      author_email='hourout@163.com',
      keywords=['jupyter_kernel', 'oracle_kernel'],
      license='Apache License Version 2.0',
      install_requires=['cx-Oracle', 'sqlalchemy', 'pandas', 'jupyter'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: System :: Shells',
      ],
      packages=['oracle_kernel'],
      zip_safe=False
)
