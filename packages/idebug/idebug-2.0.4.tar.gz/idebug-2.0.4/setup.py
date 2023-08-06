# -*- coding: utf-8 -*-
import setuptools

PKG_NAME = 'idebug'

def long_desc():
    return ''
    with open("README.md", "r") as f:
        text = f.read()
        f.close()
    return text

setuptools.setup(
    name=PKG_NAME,
    version="2.0.4",
    author="innovata sambong",
    author_email="iinnovata@gmail.com",
    description="innovata-debug",
    long_description=long_desc(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/{PKG_NAME}",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
