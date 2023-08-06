Installation Guide
==================

The Nutanix API Client is available through the Python Package Index.

The code is available on gitlab at https://gitlab.com/nutanix-se/python/ntnx-api-library and can optionally be built and installed from source.


Python Package Index Installation
---------------------------------

.. code-block:: bash

    $ pip install ntnx_api

Or

.. code-block:: bash

    $ easy_install ntnx_api


Source Code Installation
---------------------------------
.. code-block:: bash

    $ mkdir nutanix
    $ cd nutanix
    $ git clone https://gitlab.com/nutanix-se/python/ntnx-api-library
    $ cd ntnx-api-library
    $ python setup.py install

Or to build HTML documentation from source:

.. code-block:: bash

    $ cd docs/
    $ make html

This creates a _build/ directory under docs/.