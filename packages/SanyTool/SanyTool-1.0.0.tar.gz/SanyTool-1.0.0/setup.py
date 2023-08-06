#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: thao
# Mail: thao92@126.com
# Created Time:  2021-01-06 09:58:34
#############################################


from setuptools import setup, find_packages
import sys
import importlib
importlib.reload(sys)

setup(
    name = "SanyTool",
    version = "1.0.0",
    keywords = ["pip", "SanyTool", "thao"],
    description = "Common tools for model development",
    long_description = "Common tools for model development",
    license = "MIT Licence",

    url = "http://gitlab.sanywind.net/sanydata/sanytool",
    author = "thao",
    author_email = "thao92@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['numpy', 'pandas', 'arrow', 'sklearn']
#     install_requires = []
)
