"""Setup script for dbam"""

import os.path
from setuptools import setup

# file directory
HERE = os.path.abspath(os.path.dirname(__file__))

# README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# setup everything
setup(
    name="dbam",
    version="0.0.2",
    description="databamboo cli tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/databamboo/dbam",
    author="Harry Wang",
    author_email="support@databamboo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["dbam"],
    include_package_data=True,
    install_requires=[
        "importlib_resources",
    ],
    entry_points={"console_scripts": ["dbam=dbam.__main__:main"]},

)
