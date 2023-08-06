Quick Start Guide
=================

This guide is intended to give users a basic idea of REST Client usage
through examples.


Before You Begin
----------------

You should already have the Nutanix Prism REST Client installed.

This includes installing REST Client package dependencies.

See :doc:`installation` for more information.


Starting A Session
------------------

To verify the REST Client package is installed and importable, try executing
the following in a Python interpreter:

.. code-block:: python

    >>> from ntnx_api.client import ApiClient
    >>> ntnx_api = ApiClient(
    >>>   connection_type = 'pe',
    >>>   ip_address='1.1.1.1'
    >>>   username='admin'
    >>>   password='nutanix/4u'
    >>> )

If that succeeds without an ImportError, you are ready to start using the client.

.. code-block:: python

    >>> from ntnx_api import prism
    >>> ntnx_cluster = prism.Cluster(api_client=ntnx_api)
    >>> clusters = ntnx_clusters.get_clusters()
    >>> print(len(clusters))

