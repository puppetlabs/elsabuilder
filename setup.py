#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click==6.7',
    'Logbook==1.1.0',
    'Fabric==1.14.0',
    'sh==1.12.14',
]

setup_requirements = [
    'pytest-runner',
    # TODO(barleyj-puppet): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='elsabuilder',
    version='0.1.0',
    description="Python utility that executes Frankenbuilder commands on remote hosts.",
    long_description=readme + '\n\n' + history,
    author="Jayson Barley",
    author_email='jayson.barley@puppet.com',
    url='https://github.com/barleyj-puppet/elsabuilder',
    py_modules=['elsabuilder'],
    packages=find_packages(include=['elsabuilder', 'elsabuilder.*']),
    entry_points={
        'console_scripts': [
            'elsabuilder=elsabuilder.elsabuilder:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='elsabuilder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
