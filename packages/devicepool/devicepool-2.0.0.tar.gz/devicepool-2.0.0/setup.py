#!/usr/bin/python
# -*- coding: UTF-8 -*-

import setuptools


def readme():
  with open('README', 'r') as f:
    return f.read()

setuptools.setup(
	
	name='devicepool',
    version='2.0.0',
    author='Ding Yi',
    author_email='dvdface@hotmail.com',
    description='the package used to manage resources in the resource pool.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/dvdface/devicepool',
    py_modules=['devicepool'],
    license='MIT',
    test_suite='test_devicepool',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)