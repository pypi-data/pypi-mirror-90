Contributing Guide
==================

Create a private fork of the project

On master branch, increment version number

Set __version__ = '1.5.0' in ntnx_api/__version.py

Update docs/changelog.rst with new version & changes

Make changes to the ntnx_api code

Install local developer requirements

pip install -r test-requirements.txt

Run flake8 locally to verify package

.. code-block:: bash

    $ tox -e flake8

Run unit test locally to verify package. You may have to update the IP addresses in the test included in ntnx_api/test/ with an ip address of your local nutanix cluster / prism central.

.. code-block:: bash

    $ tox -e py3

Push changes

.. code-block:: bash

    $ git push origin master

Create tag for version

.. code-block:: bash

    $ git tag 1.5.0 -m "Release v1.5.0"

Push tag

.. code-block:: bash

    $ git push origin 1.5.0

Submit merge request back to develop branch of main project