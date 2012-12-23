#!/usr/bin/env python
import setuptools

with open('README.md') as file:
    long_description = file.read()

setuptools.setup(
    name="mongomonkey",
    version="0.1",
    author="Daniil Bondarev",
    author_email="xonatius@gmail.com",
    description="A MongoDB object-document mapping layer for Python",
    license="BSD",
    keywords="mongo mongodb pymongo odm orm",
    url="http://github.com/xonatius/mongo-monkey",
    packages=["mongomonkey"],
    long_description=long_description,
    install_requires=['pymongo'],
    test_suite="tests",
    )
