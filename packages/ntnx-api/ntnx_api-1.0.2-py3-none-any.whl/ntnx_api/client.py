#!/usr/bin/python
# Copyright: (c) 2020, Ross Davies <davies.ross@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
ntnx_api.client
---------------

ApiClient
^^^^^^^^^
.. autoclass:: ntnx_api.client.ApiClient
    :members:

.. autoclass:: ntnx_api.client.NutanixError

.. autoclass:: ntnx_api.client.NutanixRestHTTPError

"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from base64 import b64encode
import requests
import urllib3
import json


DOCUMENTATION = r'''
    name: nutanix_api.client
    author:
        - Ross Davies <davies.ross@gmail.com>

    short_description: Connect to the Nutanix Prism v2 or v3 API and return data

    description:
        - Connect to the API and test successful login

    requirements:
        - "python >= 3.5"
        - "requests >= 2.24.0"
'''

EXAMPLES = r'''
'''


class NutanixError(Exception):
    """Exception type raised by Nutanix API.

    :param reason: A message describing why the error occurred.
    :type reason: str

    :ivar str reason: A message describing why the error occurred.
    """

    def __init__(self, reason):
        self.reason = reason
        super(NutanixError, self).__init__(reason)

    def __str__(self):
        return "Error: {0}".format(self.reason)


class NutanixRestHTTPError(NutanixError):
    """Exception raised as a result of non-200 response status code.

    :param target: IP or DNS name of the array that received the HTTP request.
    :type target: str
    :param rest_version: The REST API version that was used when making the request.
    :type rest_version: str
    :param data: The REST API data that was used when making the request.
    :type data: str
    :param params: The REST API parameters that was used when making the request.
    :type params: str
    :param response: The response of the HTTP request that caused the error.
    :type response: :class:`requests.Response`

    :ivar str target: IP or DNS name of the array that received the HTTP request.
    :ivar str rest_version: The REST API version that was used when making the request.
    :ivar int code: The HTTP response status code of the request.
    :ivar dict headers: A dictionary containing the header information. Keys are case-insensitive.
    :ivar str reason: The textual reason for the HTTP status code (e.g. "BAD REQUEST").
    :ivar str text: The body of the response which may contain a message explaining the error.

    .. note:: The error message in text is not guaranteed to be consistent across REST versions, and thus should not be programmed against.
    """

    def __init__(self, target, rest_version, data, params, response):
        super(NutanixRestHTTPError, self).__init__(response.reason)
        self.target = target
        self.rest_version = rest_version
        self.data = data
        self.params = params
        self.code = response.status_code
        self.headers = response.headers
        self.text = response.text

    def __str__(self):
        msg = ("RestHTTPError status code {0} returned by REST "
               "version {1} at {2}:\nhttp params: {3}\nhttp body: {4}\n{5}\n{6}")
        return msg.format(self.code, self.rest_version, self.target, self.params, self.data, self.reason, self.text)


class ApiClient(object):
    """A class to represent a connection to an Nutanix API

    :param connection_type: Identifier for the type of Nutanix API to connect to
    :type connection_type: str('pe','pc','era','karbon','kps','frame','foundation')
    :param ip_address: IPv4 address or resolvable DNS entry for Nutanix API host
    :type ip_address: str
    :param username: Username to authenticate to API (default='admin')
    :type username: str, optional
    :param password: Password for user to authenticate to API (default='nutanix/4u')
    :type password: str, optional
    :param port: The port where the Nutanix API listens (default='9440')
    :type port: str, optional
    :param validate_certs: The port where the Nutanix API listens (default='9440')
    :type validate_certs: bool, optional
    :param environment: Environment string for Xi Frame
    :type environment: str, optional
    :param api_key: API Key string for Karbon Platform Services (KPS)
    :type api_key: str, optional

    :raises: :class:`ValueError`
        - If the connection type is not set
        - If the connection type is not valid

    :raises: :class:`NutanixError`
        - If the API is not reachable
    """

    def __init__(self, connection_type, ip_address=None, username="admin", password="nutanix/4u", port="9440",
                 validate_certs=False, environment=None, api_key=None):
        self.encoded_credentials = b64encode(bytes('{0}:{1}'.format(username, password), encoding='ascii')).decode('ascii')
        self.auth_header = 'Basic {0}'.format(self.encoded_credentials)

        self.validate_certs = validate_certs
        if not validate_certs:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        supported_connections = ['pe', 'pc', 'era', 'karbon', 'kps', 'frame', 'foundation']
        if connection_type not in supported_connections:
            raise ValueError('connection_type needs to be set to pe, pc, era, karbon, kps, frame, foundation not {}.'.format(connection_type))

        self.connection_type = connection_type

        if not port:
            ports = {
                'pe': '9440',
                'pc': '9440',
                'foundation': '8000',
                'frame': '443',
                'karbon': '443',  # VALIDATE
                'kpa': '443',
            }
            port = ports[connection_type]

        apis = {
            'pc': {
                'default': 'v3',
                'uris': {
                    'v1': 'https://{0}:{1}/PrismGateway/services/rest/v1'.format(ip_address, port),
                    'v2.0': 'https://{0}:{1}/PrismGateway/services/rest/v2.0'.format(ip_address, port),
                    'v3': 'https://{0}:{1}/api/nutanix/v3'.format(ip_address, port),
                },
            },
            'pe': {
                'default': 'v2.0',
                'uris': {
                    'v1': 'https://{0}:{1}/PrismGateway/services/rest/v1'.format(ip_address, port),
                    'v2.0': 'https://{0}:{1}/PrismGateway/services/rest/v2.0'.format(ip_address, port),
                },
            },
            'foundation': {
                'default': 'v1',
                'uris': {
                    'v1': 'https://{0}:{1}/foundation'.format(ip_address, port),
                },
            },
            'frame': {
                'default': 'v1',
                'uris': {
                    'v1': 'https://{0}.{1}/v1'.format(ip_address, environment),
                },
            },
            'karbon': {
                'default': 'v1',
                'uris': {
                    'v1': None,
                },
            },
            'kps': {
                'default': 'v1',
                'uris': {
                    'v1': None,
                },
            },
        }

        self.api_base = apis[connection_type]['uris']
        self._api_version = apis[connection_type]['default']

        result = self.test()
        if not result:
            raise NutanixError('API connection failed. Please check parameters and try again.')

    def request(self, uri, api_version=None, payload=None, params=None, response_code=200, timeout=120, method=None):
        """Perform HTTP request for REST API.

        :param uri: URI of resource to interact with
        :type uri: str
        :param api_version: Version of API to use. Affects the base of the called URI.
        :type api_version: str('v1', 'v2.0', 'v3'), optional
        :param payload: Data to be used in the body of request
        :type payload: dict, optional
        :param params: Data to be used in the query string of request
        :type params: dict, optional
        :param response_code: Expected response code (default=200)
        :type response_code: int, optional
        :param timeout: Number of seconds to wait before the API call times out (default=120)
        :type timeout: int, optional
        :param method: Method for the API request. If payload=None default=GET, if payload!=None default=POST
        :type method: str('GET', 'POST', 'PUT', 'DELETE'), optional

        :return: Result of API query
        :rtype: ResponseDict or ResponseList
        """
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': 'Basic {0}'.format(self.encoded_credentials), 'cache-control': 'no-cache'}

        try:
            if not api_version:
                api_version = self._api_version

            request_url = '{0}{1}'.format(self.api_base[api_version], uri)

            if self.connection_type != 'pc' and params and api_version != 'v3':
                params.pop('proxyClusterUuid')

            method = method or ('POST' if payload else 'GET')

            response = requests.request(method, request_url, headers=headers, verify=self.validate_certs,
                                        timeout=timeout, data=json.dumps(payload), params=params)

        except requests.exceptions.HTTPError:
            raise NutanixRestHTTPError(request_url, str(api_version), json.dumps(payload), params, response)

        except requests.exceptions.RequestException as err:
            raise NutanixError(err)

        except Exception as err:
            raise NutanixError(err)

        try:
            return response.json()
        except ValueError:
            return response.text

    def test(self):
        """Test that a query can be performed against the defined API connection

        :return: `True` if connected, `False` otherwise
        :rtype: bool
        """
        params = {}
        payload = None
        uri = ''

        api_test = {
            'pc': {
                'uri': '/versions',
                'payload': None,
                'params': None,
            },
            'pe': {
                'uri': '/clusters',
                'payload': None,
                'params': None,
            },
            'foundation': {
                'uri': '/version',
                'payload': None,
                'params': None,
            },
            'frame': {
                'uri': '/accounts',
                'payload': None,
                'params': None,
            },
            'karbon': {
                'uri': '/karbon/v1-alpha.1/version',
                'payload': None,
                'params': None,
            },
            'kps': {
                'uri': '/karbon/v1-alpha.1/version',
                'payload': None,
                'params': None,
            },
        }

        uri = api_test[self.connection_type]['uri']
        payload = api_test[self.connection_type]['payload']
        params = api_test[self.connection_type]['params']

        result = self.request(uri=uri, payload=payload, params=params)

        if result:
            return True
        else:
            return False
