#!/usr/bin/env python3
from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='meetg',
    version='0.1',
    packages=['meetg'],
    description='Framework for creating Telegram bots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/meequz/meetg',
    author='Mikhail Varantsou',
    license='LGPL-3.0',
    author_email='meequz@gmail.com',
    install_requires=['python-telegram-bot', 'pymongo'],
    keywords='telegram bot framework',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.5',
)
