#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from setuptools import setup

# read the contents of README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="S3Dict",
    version="0.01",
    description="python dictionary class that saves its state in a json file on an Amazon S3 bucket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rhet Turnbull",
    author_email="rturnbull+git@gmail.com",
    url="https://github.com/RhetTbull/",
    project_urls={"GitHub": "https://github.com/RhetTbull/s3dict"},
    download_url="https://github.com/RhetTbull/s3dict",
    packages=["S3Dict"],
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["boto3", "loguru"],
)
