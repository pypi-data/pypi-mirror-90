#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

README = 'D:\小马哥\编程\作品\python2\分类区1：库\easyCrawler\README.md'
with open(README, 'r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='easyCrawler',
    version='0.0.4',
    author='William Ma',
    author_email='3327821469@qq.com',
    url='https://github.com/theCoder-WM',
    description=u'An easy crawler for new hands',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['easyCrawler'],
    install_requires=['requests==2.23.0', 'bs4==0.0.1'],
    entry_points={
        'console_scripts': [

        ]
    }
)
