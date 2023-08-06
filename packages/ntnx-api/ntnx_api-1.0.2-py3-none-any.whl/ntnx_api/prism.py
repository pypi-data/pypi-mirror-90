#!/usr/bin/python
# Copyright: (c) 2020, Ross Davies <davies.ross@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
ntnx_api.prism
--------------

Config
^^^^^^
.. autoclass:: ntnx_api.prism.Config
    :members:

Cluster
^^^^^^^
.. autoclass:: ntnx_api.prism.Cluster
    :members:

Hosts
^^^^^
.. autoclass:: ntnx_api.prism.Hosts
    :members:

Vms
^^^
.. autoclass:: ntnx_api.prism.Vms
    :members:

Images
^^^^^^
.. autoclass:: ntnx_api.prism.Images
    :members:

StorageContainer
^^^^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.StorageContainer
    :members:

StorageVolume
^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.StorageVolume
    :members:
"""

from __future__ import (absolute_import, division, print_function)
import collections

__metaclass__ = type

DOCUMENTATION = r'''
    name: nutanix_api.prism
    author:
        - Ross Davies <davies.ross@gmail.com>

    short_description: Get & update data from Prism Element & Prism Central

    description:
        - Retrieve data from the API for the following API components
            - Prism UI
            - Prism Central Categories
            - Prism Central Tags
            - Clusters
            - Hosts
            - Images
            - Virtual Machines
            - Storage
                - Containers
                - Volume Groups

    requirements:
        - "python >= 3.5"
'''

EXAMPLES = r'''
'''


class Config(object):
    """A class to represent the configuration of the Nutanix Prism Instance

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.categories = []
        self.category_keys = []
        self.projects = []
        self.ui_config = {}
        self.pulse = {}
        self.smtp = {}
        self.auth_types = {}
        self.auth_directories = {}
        self.auth_dir_role_mappings = {}
        self.local_users = {}
        self.alert_config = {}
        self.auth_config = {}
        self.ntp_servers = {}
        self.dns_servers = {}
        self.proxy = {}

    def get_ui_config(self, clusteruuid=None):
        """Get the configuration data for a clusters Prism Element user interface

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        payload = None
        uri = '/application/system_data'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.ui_config = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.ui_config[clusteruuid]

    def get_categories(self):
        """Retrieve data for all categories.

        .. note:: Will only return data when `connection_type=='pc'`
        """
        params = {}

        if self.api_client.connection_type == "pc":
            uri = '/categories/list'
            payload = '{ "kind":"category", "offset": 0, "length": 2147483647  }'
            self.categories = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'entities')

        else:
            # pe does not have category data
            self.categories = {}

        return self.categories

    def get_category_keys(self, category):
        """Retrieve data for all keys belonging to a specific category.

        :param category: Category name
        :type category: str

        .. note:: Will only return data when `connection_type=='pc'`
        """
        params = {}

        if self.api_client.connection_type == "pc":
            uri = '/categories/{0}/list'.format(category)
            payload = '{ "kind":"category", "offset": 0, "length": 2147483647  }'
            self.category_keys = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'entities')

        else:
            # pe does not expose category data
            self.category_keys = {}

        return self.category_keys

    def get_category_key_usage(self, category, key):
        """Retrieve data for all vms or hosts belonging to a specific category & key.

        :parameter category: Category name
        :type category: str
        :parameter key: Key name
        :type key: str

        .. note::
            Will only return data when `connection_type=='pc'`
        """
        params = {}
        result = []

        if self.api_client.connection_type == "pc":
            uri = '/category/query'
            payload = {
                "group_member_count": 2147483647,
                "group_member_offset": 0,
                "usage_type": "APPLIED_TO",
                "category_filter": {
                    "type": "CATEGORIES_MATCH_ANY",
                    "kind_list": ["vm", "host"],
                    "params": {
                        category: key
                    }
                }
            }
            matches = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'results')

            for match in matches:
                for kind_reference in match.get('kind_reference_list'):
                    item = {
                        "name": kind_reference.get('name'),
                        "uuid": kind_reference.get('uuid'),
                        "type": match.get('kind')
                    }
                    result.append(item)

        else:
            # pe does not expose category data
            pass

        return result

    def get_projects(self):
        """Retrieve data for all projects.

        .. note:: Will only return data when `connection_type=='pc'`
        """
        params = {}

        if self.api_client == "pc":
            uri = '/projects/list'
            payload = '{ "kind":"project", "offset": 0, "length": 2147483647  }'
            self.projects = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'entities')

        else:
            # pe does not expose project data
            self.projects = {}

        return self.projects

    def get_project_usage(self, project_name):
        """Retrieve vms that belong to a specific project.

        :param project_name: Project name
        :type project_name: str

        .. note:: Will only return data when `connection_type=='pc'`
        """
        params = {}
        result = []

        if self.api_client == "pc":
            uri = '/vms/list'
            payload = '{"kind": "vm", "offset": 0, "length": 2147483647 }'
            vms = self.api_client.request(uri=uri, payload=payload, params=params)

            for vm in vms:
                if vm.get('metadata'):
                    project_kind = vm.get('metadata').get('project_reference').get('kind')
                    vm_project_name = vm.get('metadata').get('project_reference').get('name')
                    if 'project_reference' in vm.get('metadata') and project_kind == 'project' and \
                            vm_project_name == project_name:
                        item = {
                            'name': vm.get('status').get('name'),
                            'uuid': vm.get('metadata').get('uuid')
                        }
                        result.append(item)

        else:
            # pe does not expose category data
            pass

        return result

    def _add_ui_setting(self, setting_type, setting_key, setting_value, clusteruuid=None):
        """Add UI setting for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type setting_type: UI setting type
        :type setting_type: str
        :type setting_key: UI setting key
        :type setting_key: str
        :type setting_value: UI setting value
        :type setting_value: str
        """
        params = {}
        uri = '/application/system_data'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'type': setting_type,
            'key': setting_key,
            'value': setting_value,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def _update_ui_setting(self, setting_type, setting_key, setting_value, clusteruuid=None):
        """Update UI setting for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type setting_type: UI setting type
        :type setting_type: str
        :type setting_key: UI setting key
        :type setting_key: str
        :type setting_value: UI setting value
        :type setting_value: str
        """
        params = {}
        uri = '/application/system_data'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'type': setting_type,
            'key': setting_key,
            'value': setting_value,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    # UI color
    def get_ui_color(self, clusteruuid=None):
        """Get UI color 1 and color 2 for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI colors `{'color1': '#CC6164', 'color2':'#FFD055'}` or None
        :rtype: ResponseDict
        """
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        color1 = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'color_in').get('value')
        color2 = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'color_out').get('value')

        if color1 or color2:
            result = {
                'color1': color1,
                'color2': color2,
            }

        return result

    def set_ui_color(self, color1, color2, clusteruuid=None):
        """Set UI color 1 and color 2 for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type color1: First color value to set
        :type color1: str
        :type color2: Second color value to set
        :type color2: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        ui_colors = self.get_ui_color(clusteruuid=clusteruuid)
        if ui_colors.get('color1') and ui_colors.get('color1') != color2:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_in', setting_value=color1, clusteruuid=clusteruuid)
            result = 'updated'

        elif ui_colors.get('color2') and ui_colors.get('color2') != color2:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_out', setting_value=color2, clusteruuid=clusteruuid)
            result = 'updated'

        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_in', setting_value=color1, clusteruuid=clusteruuid)
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_out', setting_value=color2, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI title & blurb
    def get_ui_text(self, clusteruuid=None):
        """Get UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI text `{'title': 'blah', 'blurb':'blah blah'}` or None
        :rtype: ResponseDict
        """
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        title = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'product_title').get('value')
        blurb = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'title').get('value')

        if title or blurb:
            result = {
                'title': title,
                'blurb': blurb,
            }

        return result

    def set_ui_text(self, title, blurb, clusteruuid=None):
        """Set UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type title: Logon UI title text (Above the username/password field)
        :type title: str
        :type blurb: Logon UI blurb text (Below the username/password field)
        :type blurb: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None
        ui_text = self.get_ui_text(clusteruuid=clusteruuid)

        if ui_text.get('title') and ui_text.get('title') != title:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='product_title', setting_value=title, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='product_title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'added'

        if ui_text.get('blurb') and ui_text.get('blurb') != blurb:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI logon banner
    def get_ui_banner(self, clusteruuid=None):
        """Get UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI banner `{'status': 'true', 'content':'blah blah'}` or None
        :rtype: ResponseDict
        """
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and
                      item["key"] == 'welcome_banner_status').get('value')
        content = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and
                       item["key"] == 'welcome_banner_content').get('value')

        if status or content:
            result = {
                'status': status,
                'content': content,
            }

        return result

    def set_ui_banner(self, status, content, clusteruuid=None):
        """Set UI welcome banner (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: Logon UI banner status
        :type status: bool
        :type content: Logon UI banner content
        :type content: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        ui_banner = self.get_ui_banner(clusteruuid=clusteruuid)
        if ui_banner.get('status') and ui_banner.get('status') != status:
            self._update_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_status', setting_value=str(status), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_status', setting_value=str(status), clusteruuid=clusteruuid)
            result = 'added'

        if ui_banner.get('content') and ui_banner.get('content') != content:
            self._update_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_content', setting_value=content, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_content', setting_value=content, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI 2048 game
    def get_ui_2048_game(self, clusteruuid=None):
        """Get UI 2048 game status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI 2048 game setting `{'status': 'true'}` or None
        :rtype: ResponseDict
        """
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "UI_CONFIG" and item["key"] == 'disable_2048').get('value')

        if status:
            result = {
                'status': True,
            }
        else:
            result = {
                'status': False,
            }

        return result

    def set_ui_2048_game(self, status, clusteruuid=None):
        """Set UI 2048 game status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: 2048 game status
        :type status: bool

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        ui_2048_status = self.get_ui_2048_game(clusteruuid=clusteruuid)
        if ui_2048_status.get('status') and ui_2048_status.get('status') != status:
            self._update_ui_setting(setting_type='UI_CONFIG', setting_key='disable_2048', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='UI_CONFIG', setting_key='disable_2048', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI animation
    def get_ui_animation(self, clusteruuid=None):
        """Get UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI particle animation setting `{'status': 'true'}` or None
        :rtype: ResponseDict
        """
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and item["key"] == 'disable_video').get('value')

        if status:
            result = {
                'status': True,
            }
        else:
            result = {
                'status': False,
            }

        return result

    def set_ui_animation(self, status, clusteruuid=None):
        """Set UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: animated background particle status
        :type status: bool

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        ui_animation_status = self.get_ui_animation(clusteruuid=clusteruuid)
        if ui_animation_status.get('status') and ui_animation_status.get('status') != status:
            self._update_ui_setting(setting_type='welcome_banner', setting_key='disable_video', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='welcome_banner', setting_key='disable_video', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    def get_pulse(self, clusteruuid=None):
        """Get pulse config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing pulse configuration from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/pulse'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.pulse[clusteruuid] = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.pulse[clusteruuid]

    def update_pulse(self, enable, email_address_list=None, email_nutanix=False, clusteruuid=None):
        """Get pulse config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        """
        params = {}
        uri = '/pulse'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'enable': enable,
            'enableDefaultNutanixEmail': email_nutanix,
            'emailContactList': email_address_list,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_pulse(self, enable, email_address_list=None, email_nutanix=False, clusteruuid=None):
        """Set UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type enable: Pulse enabled
        :type enable: bool
        :type email_address_list: animated background particle status
        :type email_address_list: list, optional
        :type email_nutanix: Send pulse data to nutnaix via email
        :type email_nutanix: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if self.pulse.get(clusteruuid):
            self.get_pulse(clusteruuid=clusteruuid)

        if bool(self.pulse.get(clusteruuid).get('enable')) != enable or \
                bool(self.pulse.get(clusteruuid).get('enableDefaultNutanixEmail')) != email_nutanix or \
                self.pulse.get(clusteruuid).get('emailContactList') != email_address_list:
            self.update_pulse(enable=enable, email_nutanix=email_nutanix, email_address_list=email_address_list, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_pulse(clusteruuid=clusteruuid)

        return result

    def get_smtp(self, clusteruuid=None):
        """Get smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing smtp configuration from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/cluster/smtp'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.smtp[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.smtp[clusteruuid]

    @staticmethod
    def _get_smtp_mode(mode):
        """Return smtp mode string based on boolean value

        :param mode: SMTP mode
        :type mode: str('tls', 'ssl', None)

        :returns: Text for API smtp mode type variable defined by supplied boolean variable.
        :rtype: Str
        """

        modes = {
            'tls': 'STARTTLS',
            'ssl': 'SSL',
            None: 'NONE',
        }

        return modes[mode]

    def update_smtp(self, address, from_email_address, port, secure_mode=None, username=None, password=None, clusteruuid=None):
        """Update smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param address:
        :type address: str
        :param from_email_address:
        :type from_email_address: str
        :param port:
        :type port: int
        :param secure_mode:
        :type secure_mode: str, optional
        :param username:
        :type username: str, optional
        :param password:
        :type password: str, optional
        """
        params = {}
        uri = '/cluster/smtp'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'address': address,
            'from_email_address': from_email_address,
            'port': port,
            'secure_mode': self._get_smtp_mode(secure_mode),
        }

        if secure_mode and ((username and not password) or (password and not username)):
            raise ValueError('Secure mode defined but both username and password not provided.')
        else:
            payload['username'] = username
            payload['password'] = password

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_smtp(self, clusteruuid=None):
        """Remove smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        uri = '/cluster/smtp'
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_smtp(self, address, port, mode=None, from_email_address='do-not-reply@nutanix.cluster', username=None, password=None, force=False,
                 clusteruuid=None):
        """Set smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param address: SMTP server IP address or FQDN
        :type address: str
        :param port: SMTP server port
        :type port: int
        :param mode: SMTP connection mode
        :type mode: str('tls', 'ssl', None), optional
        :param from_email_address: Email address to send alerts from `(default: do-not-reply@nutanix.cluster)`
        :type from_email_address: str, optional
        :param username: Username to authenticate to the SMTP server
        :type username: str, optional
        :param password: Password for user to authenticate to the SMTP server
        :type password: str, optional
        :param force: Force update regardless of differences `(default=False)`
        :type force: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not self.smtp.get(clusteruuid):
            self.get_smtp(clusteruuid=clusteruuid)

        if mode and mode not in ('tls', 'ssl'):
            raise ValueError('smtp mode needs to be "tls", "ssl" or None.')

        if mode in ('tls', 'ssl') and not username and not password:
            raise ValueError('smtp modes "tls" and "ssl" require authentication. Provide a username & password.')

        # If SNMP not defined
        if not mode:
            if (self.smtp.get(clusteruuid).get('address') and self.smtp.get(clusteruuid).get('from_email_address') and self.smtp.get(clusteruuid).get(
                    'port')) or \
                    self.smtp.get(clusteruuid).get('address') != address or \
                    self.smtp.get(clusteruuid).get('from_email_address') != from_email_address or \
                    self.smtp.get(clusteruuid).get('port') != port:
                self.update_smtp(address, from_email_address, port, secure_mode=mode, username=username, password=password, clusteruuid=clusteruuid)
                result = 'updated'

        else:
            if (self.smtp.get(clusteruuid).get('address') and self.smtp.get(clusteruuid).get('from_email_address') and self.smtp.get(clusteruuid).get(
                    'port')) or \
                    self.smtp.get(clusteruuid).get('address') != address or \
                    self.smtp.get(clusteruuid).get('from_email_address') != from_email_address or \
                    self.smtp.get(clusteruuid).get('port') != port or \
                    self.smtp.get(clusteruuid).get('secure_mode') != self._get_smtp_mode(mode) or \
                    self.smtp.get(clusteruuid).get('username') != username:
                self.update_smtp(address, from_email_address, port, secure_mode=mode, username=username, password=password, clusteruuid=clusteruuid)
                result = 'added'

        if result:
            self.get_smtp(clusteruuid=clusteruuid)

        if result:
            self.get_smtp(clusteruuid=clusteruuid)

        return result

    def get_auth_types(self, clusteruuid=None):
        """Get authentication types for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        uri = '/authconfig/auth_types'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_types[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.auth_types[clusteruuid]

    def get_auth_dirs(self, clusteruuid=None):
        """Get authentication directories for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        uri = '/authconfig/directories'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_directories[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.auth_directories[clusteruuid]

    @staticmethod
    def _get_group_search_type(recursive):
        """Return group search string based on boolean value

        :param recursive: Recursive search
        :type recursive: bool

        :returns: Text for API group search type variable defined by supplied boolean variable.
        :rtype: Str
        """
        group_search_type = {
            True: 'RECURSIVE',
            False: 'NON_RECURSIVE',
        }

        return group_search_type[recursive]

    def add_auth_dir(self, name, directory_url, domain, username, password, recursive=False, directory_type='LDAP', connection_type='LDAP',
                     clusteruuid=None):
        """Add authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection
        :type connection_type: str('LDAP'), optional
        """
        params = {}
        uri = '/authconfig/directories'
        method = 'POST'

        if connection_type not in ['LDAP']:
            raise ValueError('Only "LDAP" connection types allowed.')

        if directory_type not in ['ACTIVE_DIRECTORY', 'OPEN_LDAP']:
            raise ValueError('Only "ACTIVE_DIRECTORY" and "OPEN_LDAP" directory types allowed.')

        payload = {
            'connection_type': connection_type,
            'directory_type': directory_type,
            'directory_url': directory_url,
            'domain': domain,
            'group_search_type': self._get_group_search_type(recursive=recursive),
            'name': name,
            'service_account_username': username,
            'service_account_password': password,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def update_auth_dir(self, name, directory_type, directory_url, domain, username, password, recursive=False, connection_type='LDAP', clusteruuid=None):
        """Update authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection
        :type connection_type: str('LDAP'), optional
        """
        params = {}
        uri = '/authconfig/directories'
        method = 'PUT'

        if not any(name or directory_url or domain or username or password):
            raise ValueError('Please provide all non-optional variables.')

        if connection_type not in ['LDAP']:
            raise ValueError('Only "LDAP" connection types allowed.')

        if directory_type not in ['ACTIVE_DIRECTORY', 'OPEN_LDAP']:
            raise ValueError('Only "ACTIVE_DIRECTORY" and "OPEN_LDAP" directory types allowed.')

        payload = {
            'connection_type': connection_type,
            'directory_type': directory_type,
            'directory_url': directory_url,
            'domain': domain,
            'group_search_type': self._get_group_search_type(recursive=recursive),
            'name': name,
            'service_account_username': username,
            'service_account_password': password,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_auth_dir(self, name, clusteruuid=None):
        """Remove authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        """
        params = {}
        uri = '/authconfig/directories/{0}'.format(name)
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid
        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_auth_dir(self, name, directory_type, directory_url, domain, username, password, recursive=False, connection_type='LDAP', force=False,
                     clusteruuid=None):
        """Set authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups  `(default: False)`
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection `(default: 'LDAP')`
        :type connection_type: str('LDAP'), optional
        :param force: Force directory update. Use this to update the password of the auth domain user.
        :type force: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not self.auth_directories.get(clusteruuid):
            self.get_auth_dirs(clusteruuid=clusteruuid)

        group_search_type = {
            True: 'RECURSIVE',
            False: 'NON_RECURSIVE',
        }

        # If no directories defined
        if len(self.auth_directories.get(clusteruuid)) == 0:
            self.add_auth_dir(name=name, directory_url=directory_url, domain=domain, username=username, password=password,
                              recursive=recursive, directory_type=directory_type, connection_type=connection_type)

            self.get_auth_dirs(clusteruuid=clusteruuid)
            result = 'added'

        # Update defined directory
        elif len(self.auth_directories.get(clusteruuid)) == 1 and \
                any(item for item in self.auth_directories.get(clusteruuid) if item['name'] == name and
                                                                               (item.get('directory_type') != directory_type or
                                                                                item.get('directory_url') != directory_url or
                                                                                item.get('domain') != domain or
                                                                                item.get('service_account_username') != username or
                                                                                item.get('group_search_type') == group_search_type[recursive] or
                                                                                item.get('connection_type') == connection_type
                                                                               ) or force
                    ):
            self.update_auth_dir(name=name, directory_url=directory_url, domain=domain, username=username, password=password,
                                 recursive=recursive, directory_type=directory_type, connection_type=connection_type)
            self.get_auth_dirs(clusteruuid=clusteruuid)
            result = 'updated'

        # More than 1 directory defined
        elif not len(self.auth_directories.get(clusteruuid)) > 1:
            pass

        if result:
            self.get_auth_dirs(clusteruuid=clusteruuid)

        return result

    def get_auth_dir_role_mappings(self, clusteruuid=None):
        """Get all authentication role mappings for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        role_mappings = []
        params = {}
        payload = None

        if not self.auth_directories.get(clusteruuid):
            self.get_auth_dirs(clusteruuid=clusteruuid)

        for directory in self.auth_directories.get(clusteruuid):
            uri = '/authconfig/directories/{0}/role_mappings'.format(directory.get('name'))

            if clusteruuid:
                params['proxyClusterUuid'] = clusteruuid

            role_mapping = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
            if role_mapping:
                role_mappings.extend(role_mapping)

        self.auth_dir_role_mappings[clusteruuid] = role_mappings
        return self.auth_dir_role_mappings[clusteruuid]

    @staticmethod
    def _check_auth_dir_role_mapping_directory_entity_type(directory_entity_type):
        """Check directory_entity_type string is correct

        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        """
        if directory_entity_type.upper() not in ['GROUP', 'USER']:
            raise ValueError('directory_entity_type has to be set to one of "GROUP", "USER".')

    @staticmethod
    def _get_auth_dir_role_mapping_role(cluster_admin, user_admin):
        """Return the role string based on `cluster_admin` and `user_admin` boolean inputs. `ROLE_CLUSTER_VIEWER` is always added to a user
        while `ROLE_CLUSTER_ADMIN` and `ROLE_USER_ADMIN` are optional based on inputs.

        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: Role based on boolean inputs.
        :rtype: str
        """
        if user_admin:
            role = 'ROLE_USER_ADMIN'
        elif cluster_admin:
            role = 'ROLE_CLUSTER_ADMIN'
        else:
            role = 'ROLE_CLUSTER_VIEWER'

        return role

    @staticmethod
    def _check_auth_dir_role_mapping_role(mapping_role):
        """Check mapping_role string is correct

        :param mapping_role: Type of directory entity being added.
        :type mapping_role: str('ROLE_USER_ADMIN', 'ROLE_CLUSTER_ADMIN', 'ROLE_CLUSTER_VIEWER')
        """
        if mapping_role.upper() not in ['ROLE_USER_ADMIN', 'ROLE_CLUSTER_ADMIN', 'ROLE_CLUSTER_VIEWER']:
            raise ValueError('directory_entity_type has to be set to one of "ROLE_USER_ADMIN", "ROLE_CLUSTER_ADMIN", "ROLE_CLUSTER_VIEWER".')

    def add_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Add authentication role mapping for a named authentication directory on a specific cluster. If either `cluster_admin` or `user_admin` is not set the role granted to
        this user is `ROLE_CLUSTER_VIEWER`.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'POST'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def update_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Update authentication role mapping for a named authentication directory on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'PUT'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def remove_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Delete authentication role mapping for a named authentication directory on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'DELETE'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        # self._check_auth_dir_role_mapping_role(mapping_role.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Create or update authentication role mapping for a named authentication directory on a specific cluster.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        # Check whether directory exists
        self.get_auth_dirs(clusteruuid=clusteruuid)
        if not self.auth_directories.get(clusteruuid) or \
                self.auth_directories.get(clusteruuid)[0].get('name') != directory:
            raise ValueError('Directory does not exist. Please create the directory prior to adding mappings.')

        # Check whether directory mapping exists
        if not self.auth_dir_role_mappings.get(clusteruuid):
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        # Check whether directory name & role exists
        role_mapping = next((item for item in self.auth_dir_role_mappings.get(clusteruuid) if item["directoryName"] == directory and
                             item["entityType"] == directory_entity_type and item["role"] == role), None)

        # Create new role_mapping
        if not role_mapping:
            self.add_auth_dir_role_mapping(directory=directory, directory_entities=directory_entities, directory_entity_type=directory_entity_type,
                                           cluster_admin=cluster_admin, user_admin=user_admin, clusteruuid=clusteruuid)
            result = 'added'
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        # Update existing role mapping
        elif role_mapping.get('entityType') == directory_entity_type or not all(elem in role_mapping.get('entityValues') for elem in directory_entities):
            self.update_auth_dir_role_mapping(directory=directory, directory_entities=directory_entities, directory_entity_type=directory_entity_type,
                                              cluster_admin=cluster_admin, user_admin=user_admin, clusteruuid=clusteruuid)
            result = 'updated'
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        if result:
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        return result

    def get_local_users(self, clusteruuid=None):
        """Get local users on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        uri = '/users'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.local_users[clusteruuid] = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.local_users[clusteruuid]

    @staticmethod
    def _check_user_language(language):
        """Check language string is correct

        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        """

        if language not in ['en-US', 'zh-CN', 'ja-JP']:
            raise ValueError('Region has to be set to one of "en-US", "zh-CN", "ja-JP".')

    @staticmethod
    def _build_role_list(cluster_admin=False, user_admin=False):
        """Build list of roles for user based on boolean inputs. `ROLE_CLUSTER_VIEWER` is always added to a user
        while `ROLE_CLUSTER_ADMIN` and `ROLE_USER_ADMIN` are optional based on inputs.

        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: A list of roles.
        :rtype: ResponseList
        """

        roles = ['ROLE_CLUSTER_VIEWER']
        roles = []
        if cluster_admin or user_admin:
            roles.append('ROLE_CLUSTER_ADMIN')

        if user_admin:
            roles.append('ROLE_USER_ADMIN')

        return roles

    def add_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                       user_admin=False, language='en-US', clusteruuid=None):
        """Add local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional
        """
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/users'
        method = 'POST'

        # Add User.
        self._check_user_language(language)
        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)

        payload = {
            'profile': {
                'username': username,
                'firstName': firstname,
                'lastName': lastname,
                'emailId': email,
                'password': password,
                "locale": language,
                "region": language,
            },
            'enabled': enabled,
        }

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

        # Set user roles if not 'ROLE_CLUSTER_VIEWER'
        uri = '/users/{0}/roles'.format(username)
        method = 'PUT'
        payload = roles
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def update_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                          user_admin=False, language='en-US', clusteruuid=None):
        """Update local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional
        """
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/users'
        method = 'PUT'

        # Update user
        self._check_user_language(language)
        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)
        payload = {
            'profile': {
                'username': username,
                'firstName': firstname,
                'lastName': lastname,
                'emailId': email,
                'password': password,
                "locale": language,
                "region": language,
            },
            'enabled': enabled,
        }

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

        # Update user roles if not 'ROLE_CLUSTER_VIEWER'
        uri = '/users/{0}/roles'.format(username)
        method = 'PUT'
        payload = roles
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def remove_local_user(self, username, clusteruuid=None):
        """Remove local user on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        """
        params = {}
        uri = '/users/{0}'.format(username)
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                       user_admin=False, language='en-US', clusteruuid=None):
        """Create or update local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Email address for user
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` priviliges
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not self.local_users.get(clusteruuid):
            self.get_local_users(clusteruuid=clusteruuid)

        # find local user in list of local users or None
        local_user = next((item for item in self.local_users.get(clusteruuid) if item.get('profile').get('username') == username), None)

        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)

        # user not found, add user
        if not local_user:
            self.add_local_user(username=username, password=password, firstname=firstname, lastname=lastname, email=email, enabled=enabled,
                                cluster_admin=cluster_admin, user_admin=user_admin, language=language, clusteruuid=None)
            self.get_local_users(clusteruuid=clusteruuid)
            result = 'added'

        # user config does not match, update user
        elif local_user and \
                local_user.get('profile').get('lastName') != lastname or \
                local_user.get('profile').get('emailId') != email or \
                local_user.get('profile').get('locale') != language or \
                local_user.get('profile').get('region') != language or \
                local_user.get('enabled') != enabled or \
                not all(elem in local_user.get('roles') for elem in roles):

            self.update_local_user(username=username, password=password, firstname=firstname, lastname=lastname, email=email, enabled=enabled,
                                   cluster_admin=cluster_admin, user_admin=user_admin, language=language, clusteruuid=None)
            self.get_local_users(clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_local_users(clusteruuid=clusteruuid)

        return result

    def get_alert_config(self, clusteruuid=None):
        """Get alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        params = {}
        uri = '/alerts/configuration'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.alert_config[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.alert_config[clusteruuid]

    def update_alert_config(self, email_list, enable=True, enable_default=True, enable_digest=True, nutanix_default_email='nos-alerts@nutanix.com',
                            clusteruuid=None):
        """Update alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param email_list:
        :type email_list: list of str
        :param enable:
        :type enable: bool, optional
        :param enable_default:
        :type enable_default: bool, optional
        :param enable_digest:
        :type enable_digest: bool, optional
        :param nutanix_default_email:
        :type nutanix_default_email: str, optional
        """
        params = {}
        uri = '/alerts/configuration'
        method = 'PUT'

        payload = {
            'default_nutanix_email': nutanix_default_email,
            'enable': enable,
            'enable_default_nutanix_email': enable_default,
            'enable_email_digest': enable_digest,
            'email_contact_list': email_list,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_alert_config(self, clusteruuid=None):
        """Reset alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        email_list = []
        enable = False
        enable_default = False
        enable_digest = False
        self.update_alert_config(email_list, enable, enable_default, enable_digest, clusteruuid)

    def get_auth_config(self, clusteruuid=None):
        """Retrieve authentication data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional :returns: A list of dictionaries describing the authentication configuration of the cluster.

        :returns: A list of authentication config.
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/authconfig'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_config[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.auth_config[clusteruuid]

    def get_ntp(self, clusteruuid=None):
        """Retrieve ntp servers configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters ntp servers
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/cluster/ntp_servers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.ntp_servers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.ntp_servers[clusteruuid]

    def add_ntp(self, ntp_server, clusteruuid=None):
        """Add ntp server to a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_server: IP address or hostname for a ntp server
        :type ntp_server: str
        """
        params = {}
        uri = '/cluster/ntp_servers'
        method = 'POST'
        payload = {
            "value": ntp_server
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_ntp(self, ntp_server, clusteruuid=None):
        """Remove ntp server from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_server: IP address or hostname for a ntp server
        :type ntp_server: str
        """
        params = {}
        payload = None
        uri = '/cluster/ntp_servers/{0}'.format(ntp_server)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_ntp(self, clusteruuid=None, ntp_servers=None):
        """Set ntp servers for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_servers: An ordered list of ntp servers
        :type ntp_servers: list, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not ntp_servers:
            raise ValueError('no ntp server list provided.')

        if not self.ntp_servers.get(clusteruuid):
            self.get_ntp(clusteruuid=clusteruuid)

        # If no NTP servers are defined
        if len(self.ntp_servers.get(clusteruuid)) == 0:
            for ntp_server in ntp_servers:
                self.add_ntp(ntp_server)
            result = 'added'

        # If the NTP servers are not in the right order
        elif not collections.Counter(ntp_servers) == collections.Counter(self.ntp_servers.get(clusteruuid)):
            for ntp_server in self.get_ntp(clusteruuid=clusteruuid):
                self.remove_ntp(ntp_server)
            for ntp_server in ntp_servers:
                self.add_ntp(ntp_server)
            result = 'updated'

        if result:
            self.get_ntp(clusteruuid=clusteruuid)

        return result

    def get_dns(self, clusteruuid=None):
        """Retrieve dns servers configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters dns servers
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/cluster/name_servers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.dns_servers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.dns_servers[clusteruuid]

    def add_dns(self, dns_server, clusteruuid=None):
        """Add dns server to a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_server: IP address or hostname for a dns server
        :type dns_server: str
        """
        params = {}
        uri = '/cluster/name_servers'
        method = 'POST'
        payload = {
            "value": dns_server
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_dns(self, dns_server, clusteruuid=None):
        """Remove dns server from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_server: IP address or hostname for a dns server
        :type dns_server: str
        """
        params = {}
        payload = None
        uri = '/cluster/name_servers/{0}'.format(dns_server)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_dns(self, clusteruuid=None, dns_servers=None):
        """Set dns servers for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_servers: An ordered list of dns servers
        :type dns_servers: list, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not dns_servers:
            raise ValueError('no dns server list provided.')

        if not self.dns_servers.get(clusteruuid):
            self.get_dns(clusteruuid=clusteruuid)

        if len(self.dns_servers.get(clusteruuid)) == 0:
            for dns_server in dns_servers:
                self.add_dns(dns_server)
            result = 'added'

        elif not collections.Counter(dns_servers) == collections.Counter(self.get_dns(clusteruuid=clusteruuid)):
            for dns_server in self.get_dns(clusteruuid=clusteruuid):
                self.remove_dns(dns_server)

            for dns_server in dns_servers:
                self.add_dns(dns_server)
            result = 'updated'

        if result:
            self.get_dns(clusteruuid=clusteruuid)

        return result

    def get_proxy(self, clusteruuid=None):
        """Retrieve proxy configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters dns servers
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/http_proxies'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.proxy[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.proxy[clusteruuid]

    def add_proxy(self, name, address, port, proxy_types, username=None, password=None, clusteruuid=None):
        """Add proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Descriptive name for proxy server
        :type name: str
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type proxy_types: List of proxy types
        :type proxy_types: list('http', 'https', 'socks')
        :type username: Username to authenticate to the proxy
        :type username: str
        :type password: Password to authenticate to the proxy
        :type password: str
        """
        params = {}
        payload = {
            "address": address,
            "name": name,
            "port": port,
            "proxy_types": proxy_types,
        }

        if username and password:
            payload['username'] = username
            payload['password'] = password

        uri = '/http_proxies'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=201)

    def update_proxy(self, name, address, port, proxy_types, username=None, password=None, clusteruuid=None):
        """Add proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Descriptive name for proxy server
        :type name: str
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type proxy_types: List of proxy types
        :type proxy_types: list('http', 'https', 'socks')
        :type username: Username to authenticate to the proxy
        :type username: str
        :type password: Password to authenticate to the proxy
        :type password: str
        """
        params = {}
        payload = {
            "address": address,
            "name": name,
            "port": port,
            "proxy_types": proxy_types,
        }

        if username and password:
            payload["username"] = username
            payload["password"] = password

        uri = '/http_proxies'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_proxy(self, name, clusteruuid=None):
        """Remove proxy configuration from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Name of proxy server
        :type name: str
        """
        params = {}
        payload = None
        uri = '/http_proxies/{0}'.format(name)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    # flake8: noqa: C901
    def set_proxy(self, address, port, clusteruuid=None, name='proxy', username='', password='', http=True, https=False, socks=False):
        """Set proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type name: Descriptive name for proxy server
        :type name: str, optional
        :type username: Username to authenticate to the proxy
        :type username: str, optional
        :type password: Password to authenticate to the proxy
        :type password: str, optional
        :type http: Enable http for the proxy
        :type http: bool, optional
        :type https: Enable https for the proxy
        :type https: bool, optional
        :type socks: Enable socks for the proxy
        :type socks: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        result = None

        if not address:
            raise ValueError('no proxy address provided.')

        if not port:
            raise ValueError('no proxy port provided.')

        if not self.proxy.get(clusteruuid):
            self.get_proxy(clusteruuid=clusteruuid)

        proxy_types = []

        if http:
            proxy_types.append('HTTP')
        if https:
            proxy_types.append('HTTPS')
        if socks:
            proxy_types.append('SOCKS')

        # If no proxy defined
        if not self.proxy.get(clusteruuid) or len(self.proxy.get(clusteruuid)) == 0:
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'added'

        # If more than 1 proxy , remove all proxies and add new config
        elif len(self.proxy.get(clusteruuid)) > 1:
            for configured_proxy in self.proxy.get(clusteruuid):
                self.remove_proxy(configured_proxy.get('name'))
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        # If 1 proxy defined, update if name matches
        elif len(self.proxy.get(clusteruuid)) == 1 and self.proxy.get(clusteruuid)[0].get('name') == name:
            self.update_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        # If 1 proxy defined, if name does not match remove and add new config
        elif len(self.proxy.get(clusteruuid)) == 1 and self.proxy.get(clusteruuid)[0].get('name') != name:
            self.remove_proxy(name=self.proxy.get(clusteruuid)[0].get('name'), clusteruuid=clusteruuid)
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_proxy(clusteruuid=clusteruuid)

        return result


class Cluster(object):
    """A class to represent a Nutanix Cluster

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.clusters = []
        self.cluster = {}
        self.cluster_ha = {}

    def get_all_uuids(self):
        """Retrieve a list of all clusters.

        :returns: A list of dictionaries describing the configuration of each cluster.
        :rtype: ResponseList

        .. note:: Will return all registered clusters when `connection_type=='pc'`
        .. note:: Will only return one cluster when `connection_type=='pe'`
        """
        params = {}
        payload = None

        if self.api_client.connection_type == "pc":
            uri = '/clusters/list'
            payload = {
                "kind": "cluster",
                "offset": 0,
                "length": 2147483647,
            }

        else:
            uri = '/clusters'

        clusters = self.api_client.request(uri=uri, payload=payload, params=params).get('entities')

        # Only return PE clusters ie. exclude any clusters defined as MULTICLUSTER or where the cluster name is not set
        cluster_list = []
        if self.api_client.connection_type == "pc":
            for cluster in clusters:
                if "PRISM_CENTRAL" not in cluster.get('status').get('resources').get('config').get('service_list') or \
                        cluster.get('status').get('name') != 'Unnamed':
                    cluster_list.append(cluster)
        else:
            cluster_list = clusters

        for cluster in cluster_list:
            if self.api_client.connection_type == "pc":
                self.clusters.append(cluster.get('metadata').get('uuid'))
            else:
                self.clusters.append(cluster.get('uuid'))

        return self.clusters

    def get(self, clusteruuid=None):
        """Retrieve data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :returns: A dictionary describing the configuration of the cluster.
        :rtype: ResponseDict
        """
        params = {}
        payload = None
        uri = '/cluster'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.cluster[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.cluster

    def get_ha(self, clusteruuid=None):
        """Retrieve HA data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing the HA configuration of the cluster.
        :rtype: ResponseDict

        .. note:: Cluster HA configuration will only present for cluster running the AHV hypervisor.
        """
        params = {}
        payload = None
        uri = '/ha'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.cluster_ha[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.cluster_ha[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific cluster, in a specific cluster by host uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A cluster uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found cluster.
        :rtype: ResponseDict
        """
        found = {}
        if not self.clusters:
            self.get(clusteruuid)

        for entity in self.clusters:
            if entity.get('cluster_uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific cluster, in a specific cluster by host cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A host name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found cluster.
        :rtype: ResponseDict
        """
        found = {}
        if not self.clusters:
            self.get(clusteruuid)

        for entity in self.clusters:
            if entity.get('name') == name:
                found = entity
                break

        return found


class Hosts(object):
    """A class to represent a Nutanix Clusters Hosts

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.hosts = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each host in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each host from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/hosts'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.hosts[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get(
            'entities')
        return self.hosts[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific host, in a specific cluster by host uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A host uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        found = {}
        if not self.hosts.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific host, in a specific cluster by host name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A host name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        found = {}
        if not self.hosts.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found

    def search_ip(self, ip_address, clusteruuid=None):
        """Retrieve data for a specific host, in a specific cluster by ip_address. The CVM, Hypervisor and IPMI IP addresses will be tested

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param ip_address: A host name to search for.
        :type ip_address: str, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        found = {}
        if not self.hosts.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('service_vmexternal_ip') == ip_address or entity.get('hypervisor_address') == ip_address or entity.get('ipmi_address') == ip_address:
                found = entity
                break

        return found


class Vms(object):
    """A class to represent a Nutanix Clusters Virtual Machines

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.vms = {}

    def get(self, clusteruuid=None):
        """Retrieve host data for each virtual machine in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each vm from the specified cluster.
        :rtype: ResponseList
        """
        params = {'include_vm_disk_config': 'true', 'include_vm_nic_config': 'true', 'length': '2147483647'}
        payload = None
        uri = '/vms'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.vms[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.vms[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific vm, in a specific cluster by vm uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A vm uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found vm.
        :rtype: ResponseDict
        """
        found = {}
        if not self.vms.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.vms.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific vm, in a specific cluster by vm name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A vm name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found vm.
        :rtype: ResponseDict
        """
        found = {}
        if not self.vms.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.vms.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found


class Images(object):
    """A class to represent a Nutanix Clusters Images

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.images = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each image in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each image from the specified cluster.
        :rtype: ResponseList

        .. note:: Images are only present for cluster running the AHV hypervisor.
        """
        params = {'length': '2147483647'}
        payload = None
        uri = '/images'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.images[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.images[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific image, in a specific cluster by image uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A image uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found image.
        :rtype: ResponseDict
        """
        found = {}
        if not self.images.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.images.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific image, in a specific cluster by image name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A image name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found image.
        :rtype: ResponseDict
        """
        found = {}
        if not self.images.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.images.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found


class StorageContainer(object):
    """A class to represent a Nutanix Clusters Storage Container object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.storage_containers = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each container in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each container from the specified cluster.
        :rtype: ResponseList
        """
        params = {'count': '2147483647'}
        payload = None
        uri = '/storage_containers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.storage_containers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.storage_containers[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific container, in a specific cluster by container uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A container uuid to search for.
        :type uuid: str, optional
        :returns: A dictionary describing the found container.
        :rtype: ResponseDict
        """
        found = {}
        if not self.storage_containers.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.storage_containers.get(clusteruuid):
            if entity.get('storage_container_uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific container, in a specific cluster by container uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A container name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found container.
        :rtype: ResponseDict
        """
        found = {}
        if not self.storage_containers.get(clusteruuid):
            self.get(clusteruuid)

        for entity in self.storage_containers.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found


class StorageVolume(object):
    """A class to represent a Nutanix Clusters Storage Volumes object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.volume_groups = {}
        self.volumes = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each volume group & all volumes in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        self.get_volume_groups(clusteruuid)
        self.get_volumes(clusteruuid)

    def get_volume_groups(self, clusteruuid=None):
        """Retrieve data for each volume group in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each volume group from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = None
        uri = '/volume_groups'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.volume_groups[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.volume_groups[clusteruuid]

    def search_volume_groups_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific volume group, in a specific cluster by volume group uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A volume group uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found volume group.
        :rtype: ResponseDict
        """
        found = {}
        if not self.volume_groups.get(clusteruuid):
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_volume_groups_name(self, name, clusteruuid=None):
        """Retrieve data for a specific volume group, in a specific cluster by volume group uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A volume group name to search for.
        :type name: str, optional
        :returns: A dictionary describing the found volume group.
        :rtype: ResponseDict
        """
        found = {}
        if not self.volume_groups.get(clusteruuid):
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found

    def get_volumes(self, clusteruuid=None):
        """Retrieve data for each volume in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each volume group from the specified cluster.
        :rtype: ResponseList
        """
        result = []

        if not self.volume_groups.get(clusteruuid):
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            volumes = {
                'volume_group': entity.get('name'),
                'disk_list': entity.get('disk_list'),
            }
            result.append(volumes)

        self.volumes = result
        return self.volumes
