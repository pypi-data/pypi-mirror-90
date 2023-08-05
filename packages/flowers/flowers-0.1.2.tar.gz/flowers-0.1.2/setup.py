#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='flowers',
    version='0.1.2',
    description=(
        'utils'
    ),
    author='liyuhao',
    author_email='1241225413@qq.com',
    license='Apache License 2.0',
    packages=find_packages(),
    url='https://github.com/hgliyuhao/flower',
    install_requires=[
        'pdfminer3k',
        'requests'
    ],
)
