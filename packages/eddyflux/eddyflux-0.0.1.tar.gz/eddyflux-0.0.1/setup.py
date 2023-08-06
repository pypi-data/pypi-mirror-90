#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Songyan Zhu
# Mail: sz394@exeter.ac.uk
# Created Time:  2021-01-05
#############################################


from setuptools import setup, find_packages

setup(
	name = "eddyflux",
	version = "0.0.1",
	keywords = ("eddy covariance processing", "flux"),
	description = "left blank",
	long_description = "left blank",
	license = "MIT Licence",

	url = "",
	author = "Songyan Zhu",
	author_email = "sz394@exeter.ac.uk",

	packages = find_packages(),
	include_package_data = True,
	platforms = "any",
	install_requires=[

	]
)