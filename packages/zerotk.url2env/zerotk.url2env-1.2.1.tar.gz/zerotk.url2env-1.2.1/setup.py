#!/usr/bin/env python

from os import popen
from setuptools import setup, find_packages
import re

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="zerotk.url2env",
    use_scm_version=True,

    author="Alexandre Andrade",
    author_email='kaniabi@gmail.com',
    # author="Stuart Campbell",
    # author_email="stuart@harto.org",

    url="https://github.com/zerotk/url2env",

    description="Produces env vars from Heroku-style database URLs",
    long_description=long_description,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords="postgresql shell environment",

    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "url2env=url2env:main"
        ],
    },

    install_requires=[
        'click',
    ],
    setup_requires=['setuptools_scm'],
    tests_require=[],

    license="MIT",
)
