#!/usr/bin/python

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "hxss.responsibility",
	version = "0.1.1",
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Simple implementation of `chain of responsibilities` pattern",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/hxss-python/hxss.responsibility",
	packages = setuptools.find_packages(),
	keywords = ['chain', 'responsibility', 'pattern', 'coalescing'],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
)
