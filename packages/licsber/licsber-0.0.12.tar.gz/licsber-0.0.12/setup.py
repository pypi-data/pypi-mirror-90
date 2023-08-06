#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='licsber',
    version='0.0.12',
    author='Licsber',
    author_email='licsber@gmail.com',
    url='https://www.cnblogs.com/licsber/',
    description=u'个人娱乐工具箱.',
    long_description=long_description,
    packages=[
        'licsber',
        'licsber.mail',
        'licsber.utils'
    ],
    install_requires=[
        'pymongo',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'licsber=licsber:licsber',
            'count-dir=licsber:count_dir',
            'flatten_dir=licsber:flatten_dir'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent'
    ],
    license='GPLv3'
)
