import setuptools


setuptools.setup(
    name="Mongo Monkey",
    version="0.0.3-dev",
    author="Daniil Bondarev",
    author_email="xonatius@gmail.com",
    description="A MongoDB object-document mapping layer for Python",
    license="BSD",
    keywords="mongo mongodb database pymongo odm",
    url="http://github.com/xonatius/mongo-monkey",
    packages=["mongomonkey"],
    long_description="Mongo-monkey is a MongoDB object-document mapping API for Python.",
    install_requires=['pymongo'],
    tests_require=['nose']
    )
