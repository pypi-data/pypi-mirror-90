# Copyright (C) 2020 Satish Kumar S
# License: MIT

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="pyorange",
    version="2.0.0",
    description="PyOrange - An open source, low-code machine learning library in Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pyspyder/pyorange",
    author="satish kumar",
    author_email="satishsriram369@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=required,
    #extras_require={"full": optional_required,},
)