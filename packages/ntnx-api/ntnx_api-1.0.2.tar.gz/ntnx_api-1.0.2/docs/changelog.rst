Change Log
==========

A log of changes by version and date.

.. csv-table::
    :header: "Version", "Date", "Notes"
    :widths: 10, 10, 60

    "0.0.1", "10/03/2020", "Initial Version"
    "0.0.2", "10/08/2020", "Added ntp & dns get/add/delete/set to ntnx_api.cluster"
    "0.0.3", "10/09/2020", "Added proxy get/add/delete/set to ntnx_api.cluster. Added ui_color, ui_text, ui_banner, ui_2048_game, ui_animation get/set to ntnx_api.prism"
    "0.0.4", "10/09/2020", "Added pulse get/set/update to ntnx_api.prism"
    "0.0.5", "10/12/2020", "Added smtp get/set/update/delete to ntnx_api.prism"
    "0.0.6", "10/12/2020", "Added auth_type get. Added auth_directory get/add/update/set to ntnx_api.prism. Moved multiple occurances of a dict lookup to a static function for improved code usability."
    "0.0.7", "10/12/2020", "Updated documentation for API glossary to provide headings for each class to improve navigation"
    "0.0.8", "10/12/2020", "Updated author email address & added README.rst"
    "0.0.9", "10/12/2020", "Updated docstring for auth_directory to include default values"
    "0.0.10", "10/13/2020", "Included changelog.rst in README.rst. Updated tox.ini to improve test troubleshooting. Improved error messaging to client.NutanixRestHTTPError. Resolved issue for Cluster.get_all_uuids() for connections to Prism Central where the UUIDs were being returned as None. Updated Prism.set_smtp docstring. Renamed Prism.*_auth_directory to Prism.*_auth_dir."
    "0.0.11", "10/13/2020", "Resolved issue in README.rst causing publication to pypi to fail."
    "0.0.12", "10/13/2020", "Added initial unit tests & gitlab runner in homelab for testing."
    "0.0.13", "10/14/2020", "Added directory authentication, directory role & local user add/update/delete/set to ntnx_api.prism. Added OS tags to gitlab ci to ensure tasks use correct runners. Resolved issue calling incorrect API for ntnx_api.prism.*_smtp"
    "0.0.14", "10/15/2020", "Set correct method for ntnx_api.prism.add_local_user and ntnx_api.prism.update_local_user"
    "0.0.15", "10/15/2020", "Commented out windows gitlab build step as its note required currently."
    "0.0.16", "10/15/2020", "Added alert configuration to ntnx_api.prism"
    "0.0.17", "10/15/2020", "Added SAST to gitlab-ci.yml. Added tests for all added functions."
    "1.0.0", "10/19/2020", "Release 1.0.0."
    "1.0.1", "10/20/2020", "For all set_* functions in ntnx_api.prism updated the return value to indicate whether a record has been added or updated."