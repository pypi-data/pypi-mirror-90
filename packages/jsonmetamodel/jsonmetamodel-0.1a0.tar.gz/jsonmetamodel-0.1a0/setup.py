# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="jsonmetamodel",
    author="David Scheliga",
    author_email="david.scheliga@gmx.de",
    url="https://gitlab.com/david.scheliga/jsonschemamodel",
    project_urls={
        "Source Code Repository": "https://gitlab.com/david.scheliga/jsonschemamodel",
    },
    description="Creates metaclasses for parameter definition and checking with taking"
    " respect to the jsonschema defined by https://json-schema.org/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
    ],
    keywords="jsonschema, dict, interfaces",
    package_dir={"jsonmetamodel": "jsonmetamodel"},
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "augmentedtree>=0.2a0",
        "dicthandling>=0.1b5",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
