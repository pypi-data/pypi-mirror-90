#!/usr/bin/env python3

import io
from os import path
from setuptools import setup, find_packages


setup(
    name="radicale-kalabash-auth-token",
    version='0.1.0',
    description='A token based authentication plugin for Radicale provided by Kalabash.',
    url='https://github.com/amonak/radicale-kalabash-auth-token',
    author='Alphamonak Solutions',
    author_email='amonak@alphamonak.com',
    license='MIT',
    packages=["radicale_kalabash_auth_token"],
    install_requires=['radicale', 'requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
