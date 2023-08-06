Nutanix REST 1.X SDK
====================================
This library is designed to provide a simple interface for issuing commands to Nutanix software using a REST API. It communicates with the endpoint using the python requests HTTP library.

Requirements
============
This library requires the use of python 3.6 or later and the third-party library "requests".

Capabilities
============
This library supports all functionality offered by the following APIs;
    * Nutanix Prism Central
    * Nutanix Prism Element

Documentation
=============

https://nutanix-api-library.readthedocs.io/en/latest/

Installation
============
See the installation section in the documentation at https://nutanix-api-library.readthedocs.io/en/latest/installation.html

Tests
=====
From the root directory of the repo
::

 $ tox -e py3

Changes
=========
See the project change log section in the documentation at https://nutanix-api-library.readthedocs.io/en/latest/changelog.html

Files
=====
* ntnx_api/ -- Contains library code.
* docs/ -- Contains API documentation, Makefile and conf.py.
* docs/changelog.rst -- Library change log.
* LICENSE.txt -- Library BSD 2-Clause license.
* .gitlab-ci.yml -- Gitlab CI release pipeline.
* setup.py -- build script for setuptools..
* tox.ini -- Tox configuration file.
* README.txt -- This document.
