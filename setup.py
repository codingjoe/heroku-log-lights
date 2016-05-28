#!/usr/bin/env python
from distutils.spawn import find_executable

from setuptools import find_packages, setup

PACKAGE_NAME = "heroku_loglights"
PACKAGE = __import__(PACKAGE_NAME)
GH_URL = "https://github.com/codingjoe/django-cc"

if not find_executable('hub'):
    raise RuntimeError(
        '"hub" was not found.\n'
        'Please download hup at https://hub.github.com/'
    )

setup(
    name='heroku_loglights',
    version=PACKAGE.__version__,
    description=PACKAGE.__doc__.strip(),
    url=GH_URL,
    download_url=GH_URL,
    bugtrack_url='%s/issues' % GH_URL,
    author=PACKAGE.__author__,
    author_email='info@johanneshoppe.com',
    license=PACKAGE.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hll = heroku_loglights.__main__:main',
            'heroku-log-lights = heroku_loglights.__main__:main',
        ],
    },
    install_requires=['aiohttp'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
