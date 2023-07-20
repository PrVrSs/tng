#!/usr/bin/env python3
"""pvs setup script."""
from setuptools import setup, find_packages


PROJECT_NAME = 'pvs'
PROJECT_PACKAGE_NAME = 'pvs'
PROJECT_LICENSE = ''
PROJECT_AUTHOR = ''
PROJECT_COPYRIGHT = ''
PROJECT_URL = ''
PROJECT_EMAIL = ''

PROJECT_GITHUB_USERNAME = ''
PROJECT_GITHUB_REPOSITORY = ''

PYPI_URL = ''
GITHUB_URL = ''

DOWNLOAD_URL = ''
PROJECT_URLS = {
    'Bug Reports': '',
    'Dev Docs': ''
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'aiofiles==0.4.0',
    'aiohttp==3.8.5',
    'aiopg==0.16.0',
    'click==7.0',
    'gunicorn',
    'sqlalchemy==1.3.1',
    'tox==3.7.0',
    'uvloop==0.12.2',
    'youtube-dl==2019.03.18',
    'immutables',
    'pip>=8.0.3',
]

MIN_PY_VERSION = '3.7'

setup(
    name=PROJECT_PACKAGE_NAME,
    version='0.0',
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    python_requires=f'>={MIN_PY_VERSION}',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'pvs = pvs.__main__:main'
        ]
    },
)
