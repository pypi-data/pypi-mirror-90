#! /usr/bin/env python
"""Installation script."""

from os import name
from setuptools import setup


if name == 'posix':
    DATA_FILES = [
        ('/usr/lib/systemd/system', ['ddnss@.service', 'ddnss@.timer']),
        ('/usr/lib/sysusers.d', ['ddnss.conf'])
    ]
else:
    DATA_FILES = []


setup(
    name='ddnss',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    python_requires='>=3.8',
    py_modules=['ddnss'],
    entry_points={'console_scripts': ['ddnssupd = ddnss:main']},
    data_files=DATA_FILES,
    url='https://github.com/conqp/ddnss',
    license='GPLv3',
    description='Update DynDNS hosts registered at ddnss.de.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='dnamic DNS DynDNS ddnss update script client'
)
