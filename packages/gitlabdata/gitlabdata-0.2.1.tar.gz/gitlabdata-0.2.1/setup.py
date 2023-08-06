#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ["snowflake-sqlalchemy>=1.1.10"]


setup(
    name="gitlabdata",
    version="0.2.1",
    author="GitLab Data Team",
    author_email="data@gitlab.com",
    description="GitLab Data Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gitlab-data/gitlab-data-utils",
    packages=find_packages(),
    install_requires=requires,
)
