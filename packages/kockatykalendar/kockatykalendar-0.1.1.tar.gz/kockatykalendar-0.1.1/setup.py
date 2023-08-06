import os

from setuptools import find_packages
from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kockatykalendar",
    version="0.1.1",
    url="https://github.com/kockatykalendar/python",
    license='MIT',

    author="Adam Zahradník",
    author_email="adam@zahradnik.xyz",

    description="API, tools and utilities for working with KockatyKalendar.sk",
    long_description=long_description,

    packages=find_packages(exclude=('tests',)),

    install_requires=[],
    extras_require={
        "django": ["django>=1.7"],
        "api": ["requests>=2.0.0"]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
