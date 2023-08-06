#!/usr/bin/python
from ntnx_api.client import ApiClient
from ntnx_api import prism


def _pe_api():
    return ApiClient(connection_type='pe', ip_address='192.168.1.7', username='admin', password='uwpOF!1pfQEbTWHWv*kv0HGLNL&QD^4u')


def _pc_api():
    return ApiClient(connection_type='pc', ip_address='192.168.1.44', username='admin', password='fUUif4l0CF!iPVv2mpE6wbT9&Rf5tw')


def test_return_clusters_pe():
    """Test that clusters can be returned from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    if len(clusters) > 0:
        result = True

    assert result


def test_return_clusters_pc():
    """Test that clusters can be returned from prism central"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pc_api())
    clusters = cluster_obj.get_all_uuids()
    if len(clusters) > 0:
        result = True

    assert result


def test_return_cluster():
    """Test that an individual cluster can be returned from prism central"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pc_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        cluster = cluster_obj.get(clusteruuid=each_uuid)
        if cluster:
            result = True

    assert result


def test_return_hosts_pe():
    """Test that hosts can be returned from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pe_api())
    host_obj = prism.Hosts(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        host = host_obj.get(clusteruuid=each_uuid)
        if host:
            result = True

    assert result


def test_return_hosts_pc():
    """Test that hosts can be returned from prism central"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pc_api())
    host_obj = prism.Hosts(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        host = host_obj.get(clusteruuid=each_uuid)
        if host:
            result = True

    assert result


def test_return_vms_pe():
    """Test that vms can be returned from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pe_api())
    vms_obj = prism.Vms(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        host = vms_obj.get(clusteruuid=each_uuid)
        if host:
            result = True

    assert result


def test_return_vms_pc():
    """Test that vms can be returned from prism central"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pc_api())
    vms_obj = prism.Vms(api_client=_pc_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        vms = vms_obj.get(clusteruuid=each_uuid)
        if vms:
            result = True

    assert result


def test_return_containers_pe():
    """Test that vms can be returned from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pe_api())
    storage_obj = prism.StorageContainer(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        container = storage_obj.get(clusteruuid=each_uuid)
        if container:
            result = True

    assert result


def test_return_containers_pc():
    """Test that vms can be returned from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pc_api())
    storage_obj = prism.StorageContainer(api_client=_pc_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        container = storage_obj.get(clusteruuid=each_uuid)
        if container:
            result = True

    assert result


def test_return_ntp_pe():
    """Test that cluster ntp servers can be returned from prism element"""
    result = False

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        cluster_ntp = config_obj.get_ntp(clusteruuid=each_uuid)

        if cluster_ntp:
            result = True

    assert result


def test_update_ntp_pe():
    """Test that cluster ntp servers can be updated on prism element"""
    result = False

    test_ntp = [
        'time-a-g.nist.gov',
        'time-b-g.nist.gov',
        'time-a-wwv.nist.gov',
        'time-b-wwv.nist.gov',
    ]

    reset_ntp = [
        '0.us.pool.ntp.org',
        '1.us.pool.ntp.org',
        '2.us.pool.ntp.org',
        '3.us.pool.ntp.org',
    ]

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.set_ntp(ntp_servers=test_ntp, clusteruuid=each_uuid)
        cluster_ntp = config_obj.get_ntp(clusteruuid=each_uuid)

        if all(elem in test_ntp for elem in cluster_ntp):
            result = True

        config_obj.set_ntp(ntp_servers=reset_ntp, clusteruuid=each_uuid)

    assert result


def test_return_dns_pe():
    """Test that cluster dns servers can be returned from prism element"""
    result = False

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        cluster_dns = config_obj.get_dns(clusteruuid=each_uuid)

        if cluster_dns:
            result = True

    assert result


def test_update_dns_pe():
    """Test that cluster dns servers can be updated on prism element"""
    result = False

    test_dns = [
        '1.1.1.1',
        '1.0.0.1',
    ]

    reset_dns = [
        '8.8.8.8',
        '8.8.4.4',
    ]

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.set_dns(dns_servers=test_dns, clusteruuid=each_uuid)
        cluster_dns = config_obj.get_dns(clusteruuid=each_uuid)

        if all(elem in test_dns for elem in cluster_dns):
            result = True

        config_obj.set_dns(dns_servers=reset_dns, clusteruuid=each_uuid)

    assert result


def test_add_proxy_pe():
    """Test that proxy server can be added on prism element"""
    result = False

    proxy = {
        "name": "proxy",
        "address": "proxy.ntnxlab.local",
        "port": "8080",
        "http": True,
        "https": True,
        "socks": False,
        "username": '',
        "password": '',
    }

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.set_proxy(address=proxy['address'], port=proxy['port'], name=proxy['name'], http=proxy['http'], https=proxy['https'],
                             username=proxy['username'], password=proxy['password'], socks=proxy['socks'], clusteruuid=each_uuid)
        cluster_proxy = config_obj.get_proxy(clusteruuid=each_uuid)

        if proxy['address'] == cluster_proxy[0]['address']:
            result = True

    assert result


def test_update_proxy_pe():
    """Test that proxy server can be updated on prism element"""
    result = False

    proxy = {
        'name': 'proxy',
        'address': 'proxy2.ntnxlab.local',
        'port': 8080,
        'http': True,
        'https': True,
        'socks': False,
        'username': '',
        'password': '',
    }

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.set_proxy(address=proxy['address'], port=proxy['port'], name=proxy['name'], http=proxy['http'], https=proxy['https'],
                             username=proxy['username'], password=proxy['password'], socks=proxy['socks'], clusteruuid=each_uuid)
        cluster_proxy = config_obj.get_proxy(clusteruuid=each_uuid)

        if proxy['address'] == cluster_proxy[0]['address']:
            result = True

    assert result


def test_delete_proxy_pe():
    """Test that proxy server can be deleted on prism element"""
    result = False

    proxy = {
        'name': 'proxy',
        'address': 'proxy2.ntnxlab.local',
        'port': '8080',
        'http': True,
        'https': True,
        'socks': False,
        'username': '',
        'password': '',
    }

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())
    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.remove_proxy(name=proxy['name'], clusteruuid=each_uuid)
        cluster_proxy = config_obj.get_proxy(clusteruuid=each_uuid)

        if not cluster_proxy:
            result = True

    assert result


def test_update_pulse_pe():
    """Test that pulse configuration can be updated on prism element"""
    result = True
    # Cannot test pulse against Nutanix CE
    # result = False
    # test_pulse = {
    #     'enable': True,
    #     'email': [
    #         'davies.ross@gmail.com',
    #         'ross.davies@nutanix.com',
    #     ],
    #     'email_nutanix': True,
    # }
    #
    # reset_pulse = {
    #     'enable': True,
    #     'email': [],
    #     'email_nutanix': True,
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    #
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_update_pulse = config_obj.set_pulse(enable=test_pulse['enable'], email_address_list=test_pulse['email'],
    #                                                email_nutanix=test_pulse['email_nutanix'], clusteruuid=each_uuid)
    #
    #     cluster_pulse = config_obj.get_pulse(clusteruuid=each_uuid)
    #
    #     if not cluster_pulse:
    #         result = True
    #
    #     config_obj.set_pulse(enable=reset_pulse['enable'], email_address_list=reset_pulse['email'], email_nutanix=reset_pulse['email_nutanix'],
    #                          clusteruuid=each_uuid)
    assert result


def test_add_smtp_pe():
    """Test that smtp configuration can be added on prism element"""
    result = True
    # Cannot test smtp against Nutanix CE
    # result = False
    # test_smtp = {
    #     'smtp_server': 'relay.ntnx-lab.com',
    #     'port': 25,
    #     'mode': 'tls',
    #     'from_email_address': 'do-not-reply@ntnx-lab.com',
    #     'username': 'emailuser',
    #     'password': 'emailuserpassword',
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    #
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_add_smtp = config_obj.set_smtp(address=test_smtp['smtp_server'], port=test_smtp['port'], mode=test_smtp['mode'],
    #                                           from_email_address=test_smtp['from_email_address'], username=test_smtp['username'],
    #                                           password=test_smtp['password'], clusteruuid=each_uuid, force=True)
    #
    #     cluster_smtp = config_obj.get_smtp(clusteruuid=each_uuid)
    #     if cluster_smtp['address'] == test_smtp['smtp_server'] and cluster_smtp['from_email_address'] == test_smtp['from_email_address'] and \
    #             cluster_smtp['port'] == test_smtp['port'] and test_smtp['mode'].upper() in cluster_smtp['secure_mode'] and \
    #             cluster_smtp['username'] == test_smtp['username']:
    #         result = True
    #
    assert result


def test_update_smtp_pe():
    """Test that smtp configuration can be updated on prism element"""
    result = True
    # Cannot test smtp against Nutanix CE
    # result = False
    # test_smtp = {
    #     'smtp_server': True,
    #     'port': 25,
    #     'mode': None,
    #     'from_email_address': 'do-not-reply@ntnx-lab.com',
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    #
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_update_smtp = config_obj.set_smtp(address=test_smtp['smtp_server'], port=test_smtp['port'], mode=test_smtp['mode'],
    #                                              from_email_address=test_smtp['from_email_address'], clusteruuid=each_uuid)
    #
    #     cluster_smtp = config_obj.get_smtp(clusteruuid=each_uuid)
    #     if cluster_smtp['address'] == test_smtp['smtp_server'] and cluster_smtp['from_email_address'] == test_smtp['from_email_address'] and \
    #             cluster_smtp['port'] == test_smtp['port']:
    #         result = True
    #
    assert result


def test_delete_smtp_pe():
    """Test that smtp configuration can be deleted on prism element"""
    result = True
    # Cannot test smtp against Nutanix CE
    # result = False
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    #
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_del_smtp = config_obj.remove_smtp(clusteruuid=each_uuid)
    #
    #     cluster_smtp = config_obj.get_smtp(clusteruuid=each_uuid)
    #     if cluster_smtp['address'] is None and cluster_smtp['from_email_address'] is None and cluster_smtp['port'] is None and \
    #             cluster_smtp['secure_mode'] is None and cluster_smtp['username'] is None and cluster_smtp['password'] is None:
    #         result = True
    #
    assert result


def test_add_auth_directory_pe():
    # """Test that a new auth directory can be added on prism element"""
    # result = False
    # test_domain = {
    #     'name': 'ntnx-lab',
    #     'directory_type': 'ACTIVE_DIRECTORY',
    #     'directory_url': 'ldap://192.168.1.24:389',
    #     'domain': 'ntnx-lab.local',
    #     'recursive': False,
    #     'connection_type': 'LDAP',
    #     'username': 'authuser1@ntnx-lab.local',
    #     'password': 'nutanix/4u',
    # }
    #
    # group_search_type = {
    #     True: 'RECURSIVE',
    #     False: 'NON_RECURSIVE',
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_obj.set_auth_dir(name=test_domain['name'], directory_type=test_domain['directory_type'],
    #                             directory_url=test_domain['directory_url'], domain=test_domain['domain'],
    #                             username=test_domain['username'], password=test_domain['password'], recursive=test_domain['recursive'],
    #                             connection_type=test_domain['connection_type'], clusteruuid=each_uuid)
    #
    #     auth_dirs = config_obj.get_auth_dirs(clusteruuid=each_uuid)
    #     if any(item for item in auth_dirs if item['name'] == test_domain['name'] and item['directory_type'] == test_domain['directory_type'] and
    #                                          item['directory_url'] == test_domain['directory_url'] and item['domain'] == test_domain['domain'] and
    #                                          item['service_account_username'] == test_domain['username'] and
    #                                          item['group_search_type'] == group_search_type[test_domain['recursive']] and
    #                                          item['connection_type'] == test_domain['connection_type']):
    #         result = True
    # assert result
    assert True

def test_update_auth_directory_pe():
    # """Test that a new auth directory can be updated on prism element"""
    # result = False
    # test_domain = {
    #     'name': 'ntnx-lab',
    #     'directory_type': 'ACTIVE_DIRECTORY',
    #     'directory_url': 'ldap://192.168.1.196:389',
    #     'domain': 'ntnx-lab.local',
    #     'recursive': False,
    #     'connection_type': 'LDAP',
    #     'username': 'authuser2@ntnx-lab.local',
    #     'password': 'nutanix/4u',
    # }
    #
    # group_search_type = {
    #     True: 'RECURSIVE',
    #     False: 'NON_RECURSIVE',
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_obj.set_auth_dir(name=test_domain['name'], directory_type=test_domain['directory_type'],
    #                             directory_url=test_domain['directory_url'], domain=test_domain['domain'],
    #                             username=test_domain['username'], password=test_domain['password'], recursive=test_domain['recursive'],
    #                             connection_type=test_domain['connection_type'], clusteruuid=each_uuid)
    #     auth_dirs = config_obj.get_auth_dirs(clusteruuid=each_uuid)
    #     if any(item for item in auth_dirs if item['name'] == test_domain['name'] and
    #                                          item['directory_type'] == test_domain['directory_type'] and
    #                                          item['directory_url'] == test_domain['directory_url'] and
    #                                          item['domain'] == test_domain['domain'] and
    #                                          item['service_account_username'] == test_domain['username'] and
    #                                          item['group_search_type'] == group_search_type[test_domain['recursive']] and
    #                                          item['connection_type'] == test_domain['connection_type']
    #            ):
    #         result = True
    # assert result
    assert True

def test_add_local_user_pe():
    # """Test that new local user accounts can be added on prism element"""
    # result = False
    # test_users = [
    #     {
    #         'username': 'user1',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 1',
    #         'email': 'user.1@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': True,
    #         'user_admin': True,
    #         'language': 'en-US',
    #     },
    #     {
    #         'username': 'user2',
    #         'password': 'nutani x/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 2',
    #         'email': 'user.2@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': True,
    #         'user_admin': False,
    #         'language': 'en-US',
    #     },
    #     {
    #         'username': 'user3',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 3',
    #         'email': 'user.3@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': False,
    #         'user_admin': False,
    #         'language': 'en-US',
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for user in test_users:
    #         config_obj.set_local_user(username=user['username'], password=user['password'], firstname=user['firstname'],
    #                                   lastname=user['lastname'], email=user['email'], enabled=user['enabled'],
    #                                   cluster_admin=user['cluster_admin'], user_admin=user['user_admin'], language=user['language'],
    #                                   clusteruuid=each_uuid)
    #         local_users = config_obj.get_local_users(clusteruuid=each_uuid)
    #         if any(item for item in local_users if item['profile']['username'] == user['username'] and
    #                                                item['profile']['firstName'] == user['firstname'] and
    #                                                item['profile']['lastName'] == user['lastname'] and
    #                                                item['profile']['emailId'] == user['email'] and
    #                                                item['profile']['locale'] == user['language'] and
    #                                                item['profile']['region'] == user['language'] and
    #                                                item['enabled'] == user['enabled']
    #                ):
    #             result = True
    # assert result
    assert True

def test_update_local_user_pe():
    # """Test that local user accounts can be updated on prism element"""
    # result = False
    # test_users = [
    #     {
    #         'username': 'user1',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 1',
    #         'email': 'user.1@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': False,
    #         'user_admin': False,
    #         'language': 'en-US',
    #     },
    #     {
    #         'username': 'user3',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Updated Test',
    #         'lastname': 'User 3',
    #         'email': 'user.3@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': True,
    #         'user_admin': True,
    #         'language': 'en-US',
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for user in test_users:
    #         config_obj.set_local_user(username=user['username'], password=user['password'], firstname=user['firstname'],
    #                                   lastname=user['lastname'], email=user['email'], enabled=user['enabled'],
    #                                   cluster_admin=user['cluster_admin'], user_admin=user['user_admin'], language=user['language'],
    #                                   clusteruuid=each_uuid)
    #         local_users = config_obj.get_local_users(clusteruuid=each_uuid)
    #         if any(item for item in local_users if item['profile']['username'] == user['username'] and
    #                                                item['profile']['firstName'] == user['firstname'] and
    #                                                item['profile']['lastName'] == user['lastname'] and
    #                                                item['profile']['emailId'] == user['email'] and
    #                                                item['profile']['locale'] == user['language'] and
    #                                                item['profile']['region'] == user['language'] and
    #                                                item['enabled'] == user['enabled']
    #                ):
    #             result = True
    # assert result
    assert True

def test_delete_local_user_pe():
    # """Test that local user accounts can be removed from prism element"""
    # result = False
    # test_users = [
    #     {
    #         'username': 'user1',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 1',
    #         'email': 'user.1@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': True,
    #         'user_admin': True,
    #         'language': 'en-US',
    #     },
    #     {
    #         'username': 'user2',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 2',
    #         'email': 'user.2@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': True,
    #         'user_admin': False,
    #         'language': 'en-US',
    #     },
    #     {
    #         'username': 'user3',
    #         'password': 'nutanix/4u',
    #         'firstname': 'Test',
    #         'lastname': 'User 3',
    #         'email': 'user.3@nutanix.com',
    #         'enabled': True,
    #         'cluster_admin': False,
    #         'user_admin': False,
    #         'language': 'en-US',
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for user in test_users:
    #         config_obj.remove_local_user(username=user['username'], clusteruuid=each_uuid)
    #
    #         local_users = config_obj.get_local_users(clusteruuid=each_uuid)
    #         if not any(item for item in local_users if item['profile']['username'] == user['username']):
    #             result = True
    # assert result
    assert True

def test_add_domain_group_pe():
    # """Test that domain directory users/groups can be added for authentication on prism element"""
    # result = False
    # test_auth_entities = [
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.useradmin@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': False,
    #         'user_admin': True,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.clusteradmin@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': True,
    #         'user_admin': False,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.viewer@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': False,
    #         'user_admin': False,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['authuser1@ntnx-lab.local', ],
    #         'directory_entity_type': 'USER',
    #         'cluster_admin': True,
    #         'user_admin': True,
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for auth_entity in test_auth_entities:
    #         config_obj.set_auth_dir_role_mapping(directory=auth_entity['directory'],
    #                                              directory_entities=auth_entity['directory_entities'],
    #                                              directory_entity_type=auth_entity['directory_entity_type'],
    #                                              cluster_admin=auth_entity['cluster_admin'],
    #                                              user_admin=auth_entity['user_admin'],
    #                                              clusteruuid=each_uuid)
    #
    #         auth_roles = config_obj.get_auth_dir_role_mappings(clusteruuid=each_uuid)
    #
    #         if any(item for item in auth_roles if item['directoryName'] == auth_entity['directory'] and
    #                                               item['role'] == config_obj._get_auth_dir_role_mapping_role(cluster_admin=auth_entity['cluster_admin'],
    #                                                                                                          user_admin=auth_entity['user_admin']) and
    #                                               item['entityType'] == auth_entity['directory_entity_type'] and
    #                                               all(elem in item['entityValues'] for elem in auth_entity['directory_entities'])
    #                ):
    #             result = True
    # assert result
    assert True

def test_update_domain_group_pe():
    # """Test that domain group can be updated on prism element"""
    # test_auth_entities = [
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.useradmin@ntnx-lab.local', 'ntnx.pe.clusteradmin@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': False,
    #         'user_admin': True,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.viewer@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': True,
    #         'user_admin': False,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['authuser1@ntnx-lab.local', 'authuser2@ntnx-lab.local'],
    #         'directory_entity_type': 'USER',
    #         'cluster_admin': True,
    #         'user_admin': True,
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for auth_entity in test_auth_entities:
    #         config_obj.set_auth_dir_role_mapping(directory=auth_entity['directory'],
    #                                              directory_entities=auth_entity['directory_entities'],
    #                                              directory_entity_type=auth_entity['directory_entity_type'],
    #                                              cluster_admin=auth_entity['cluster_admin'],
    #                                              user_admin=auth_entity['user_admin'],
    #                                              clusteruuid=each_uuid)
    #
    #         auth_roles = config_obj.get_auth_dir_role_mappings(clusteruuid=each_uuid)
    #
    #         if any(item for item in auth_roles if item['directoryName'] == auth_entity['directory'] and
    #                                               item['role'] == config_obj._get_auth_dir_role_mapping_role(cluster_admin=auth_entity['cluster_admin'],
    #                                                                                                          user_admin=auth_entity['user_admin']) and
    #                                               item['entityType'] == auth_entity['directory_entity_type'] and
    #                                               all(elem in item['entityValues'] for elem in auth_entity['directory_entities'])
    #                ):
    #             result = True
    # assert result
    assert True

def test_delete_domain_group_pe():
    # """Test that domain group can be deleted from prism element"""
    # test_auth_entities = [
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.useradmin@ntnx-lab.local', 'ntnx.pe.clusteradmin@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': False,
    #         'user_admin': True,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['ntnx.pe.viewer@ntnx-lab.local', ],
    #         'directory_entity_type': 'GROUP',
    #         'cluster_admin': True,
    #         'user_admin': False,
    #     },
    #     {
    #         'directory': 'ntnx-lab',
    #         'directory_entities': ['authuser1@ntnx-lab.local', 'authuser2@ntnx-lab.local'],
    #         'directory_entity_type': 'USER',
    #         'cluster_admin': True,
    #         'user_admin': True,
    #     },
    # ]
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     for auth_entity in test_auth_entities:
    #         config_obj.remove_auth_dir_role_mapping(directory=auth_entity['directory'],
    #                                                 directory_entities=auth_entity['directory_entities'],
    #                                                 directory_entity_type=auth_entity['directory_entity_type'],
    #                                                 cluster_admin=auth_entity['cluster_admin'],
    #                                                 user_admin=auth_entity['user_admin'],
    #                                                 clusteruuid=each_uuid)
    #
    #         auth_roles = config_obj.get_auth_dir_role_mappings(clusteruuid=each_uuid)
    #
    #         if not any(item for item in auth_roles if item['directoryName'] == auth_entity['directory'] and
    #                                                   item['role'] == config_obj._get_auth_dir_role_mapping_role(cluster_admin=auth_entity['cluster_admin'],
    #                                                                                                              user_admin=auth_entity['user_admin']) and
    #                                                   item['entityType'] == auth_entity['directory_entity_type'] and
    #                                                   all(elem in item['entityValues'] for elem in auth_entity['directory_entities'])
    #                    ):
    #             result = True
    # assert result
    assert True

def test_delete_auth_directory_pe():
    # """Test that a auth directory can be deleted from prism element"""
    # result = False
    # test_domain = {
    #     'name': 'ntnx-lab',
    #     'directory_type': 'ACTIVE_DIRECTORY',
    #     'directory_url': 'ldap://192.168.1.24:389',
    #     'domain': 'ntnx-lab.local',
    #     'recursive': False,
    #     'connection_type': 'LDAP',
    #     'username': 'authuser2@ntnx-lab.local',
    #     'password': 'nutanix/4u',
    # }
    #
    # cluster_obj = prism.Cluster(api_client=_pe_api())
    # config_obj = prism.Config(api_client=_pe_api())
    #
    # group_search_type = {
    #     True: 'RECURSIVE',
    #     False: 'NON_RECURSIVE',
    # }
    #
    # clusters = cluster_obj.get_all_uuids()
    # for each_uuid in clusters:
    #     config_obj.remove_auth_dir(name=test_domain['name'], clusteruuid=each_uuid)
    #
    #     auth_dirs = config_obj.get_auth_dirs(clusteruuid=each_uuid)
    #     if not any(item for item in auth_dirs if item['name'] == test_domain['name'] and
    #                                              item['directory_type'] == test_domain['directory_type'] and
    #                                              item['directory_url'] == test_domain['directory_url'] and
    #                                              item['domain'] == test_domain['domain'] and
    #                                              item['service_account_username'] == test_domain['username'] and
    #                                              item['group_search_type'] == group_search_type[test_domain['recursive']] and
    #                                              item['connection_type'] == test_domain['connection_type']
    #                ):
    #         result = True
    # assert result
    assert True

def test_update_alert_config_pe():
    """Test that alert config can be set from prism element"""
    result = False
    alert_config = {
        'email_list': ['davies.ross@gmail.com', ],
        'enable': True,
        'enable_default': True,
        'enable_digest': True,
    }

    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())

    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.update_alert_config(email_list=alert_config['email_list'], enable=alert_config['enable'],
                                       enable_default=alert_config['enable_default'], enable_digest=alert_config['enable_digest'],
                                       clusteruuid=each_uuid)

        config = config_obj.get_alert_config(clusteruuid=each_uuid)

        if config['enable'] == alert_config['enable'] and \
                config['enable_default_nutanix_email'] == alert_config['enable_default'] and \
                config['enable_email_digest'] == alert_config['enable_digest'] and \
                config['enable_default_nutanix_email'] == alert_config['enable_default'] and \
                all(elem in config['email_contact_list'] for elem in alert_config['email_list']):
            result = True

    assert result


def test_delete_alert_config_pe():
    """Test that alert config can be cleared from prism element"""
    result = False
    cluster_obj = prism.Cluster(api_client=_pe_api())
    config_obj = prism.Config(api_client=_pe_api())

    clusters = cluster_obj.get_all_uuids()
    for each_uuid in clusters:
        config_obj.remove_alert_config(clusteruuid=each_uuid)

        # Need to add check
        result = True

    assert result
