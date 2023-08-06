#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["Django >= 1.11", "django-allauth"]

setup(
    name="wca-django-allauth",
    version="1.0.1",
    description="World Cube Association OAuth2 provider for django-allauth.",
    long_description=readme,
    author="Dhan-Rheb Belza",
    author_email="dhanrheb@gmail.com",
    url="https://github.com/drfb/wca-django-allauth",
    license="MIT license",
    packages=find_packages(include=["wca_allauth", "wca_allauth.*"]),
    keywords="world cube association allauth",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
    install_requires=requirements,
    include_package_data=True,
)
