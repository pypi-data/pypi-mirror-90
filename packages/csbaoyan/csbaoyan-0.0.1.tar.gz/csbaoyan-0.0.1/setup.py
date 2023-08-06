#!/usr/bin/env python
# coding: utf-8

from setuptools import setup


setup(
    name='csbaoyan',
    version='0.0.1',
    author='csbaoyan',
    author_email='csbaoyan@nonexist.com',
    url='https://csbaoyan.nonexist',
    description=u'计算机保研交流群',
    packages=['csbaoyan'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'csbaoyan=csbaoyan:csbaoyan',
        ]
    }
)