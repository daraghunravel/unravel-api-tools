#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='unravel-api-tools',
    version='0.0.1',
    description="Tools for interacting with the Unravel API",
    author="Unravel",
    author_email='mail@unravel.io',
    url='https://github.com/UnravelAnalytics/unravel-api-tools',
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'submit-unravel-test=unravel_api_tools.submit:main',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'ruamel.yaml',
    ],
    license="All Rights Reserved",
    zip_safe=False,
    keywords='unravel',
)
