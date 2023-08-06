#!/usr/bin/env python3

"""
Python3 bindings for the Nexpose API v3
"""
from collections import namedtuple
from datetime import datetime, timedelta
import urllib3

import requests

import nexpose.get_credentials as get_credentials

urllib3.disable_warnings()

class NexposeException(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        print(self.status_code)
        print(self.message)


class ResponseNotOK(NexposeException):
    """
    Request did not return 200 (OK)
    """


def _require_response_200_ok(response):
    """
    Accept a requests.response object.
    Raise ResponseNotOK if status code is not 200.
    Otherwise, return True
    """
    if response.status_code != 200:
        raise ResponseNotOK(
            status_code=response.status_code, message=response.text
        )
    return True


def config(args):
    """
    Accept args (argparser Namespace).
    Return nexpose.login
    """
    base_url = ':'.join([args.baseurl, args.port])
    
    user = args.user or get_credentials.user()
    password = args.password or get_credentials.password()
    return login(
        base_url=base_url,
        user=user,
        password=password,
        verify=args.verify,
    )


def login(*, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings),
    optionally verify (Boolean default True).
    Return a named tuple used for Nexpose login.
    """
    l = namedtuple("Login", ['base_url', 'user', 'password', 'verify'])
    return l(base_url=base_url, user=user, password=password, verify=verify)


def get(*, nlogin, endpoint, params=[]):
    """
    Accept named args nlogin (nexpose.login), endpoint (string), optional params.
    Return get against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.get(
        url,
        auth=(nlogin.user, nlogin.password),
        headers=head,
        verify=nlogin.verify,
        params=params
    )
    _require_response_200_ok(response)

    return response.json()


def delete(*, nlogin, endpoint):
    """
    Accept named args nlogin (nexpose.login) and endpoint (string)
    Return delete against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.delete(
        url, auth=(nlogin.user, nlogin.password), headers=head, verify=nlogin.verify
    )
    _require_response_200_ok(response)

    return response.json()


def put(*, nlogin, endpoint, data=[]):
    """
    Accept named args nlogin (nexpose.login) and endpoint (string)
    Return put against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.put(
        url, auth=(nlogin.user, nlogin.password), headers=head, verify=nlogin.verify, data=data,
    )
    _require_response_200_ok(response)

    return response.json()


def engines(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return scan engines resources.
    """
    return get(nlogin=nlogin, endpoint="api/3/scan_engines")['resources']


def engine_pools(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return pools resources.
    """
    return get(nlogin=nlogin, endpoint="api/3/scan_engine_pools")['resources']


def reports(*, nlogin, page=0, size=10):
    """
    Accept named args nlogin (nexpose.login), page, size (int).
    Return paginated reports response.
    """
    params = {'page': page, 'size': size}
    return get(nlogin=nlogin, endpoint="api/3/reports", params=params)


def report_history(*, nlogin, report_id):
    """
    Accept named args nlogin (nexpose.login), report_id (int).
    Return report history reponse.
    """
    return get(nlogin=nlogin, endpoint=f"api/3/reports/{report_id}/history")


def delete_report(*, nlogin, report_id):
    """
    Accept named args nlogin (nexpose.login), report_id (int).
    Return deleted report response.
    """
    return delete(nlogin=nlogin, endpoint=f"api/3/reports/{report_id}")


def scans(*, nlogin, page=0, size=10):
    """
    Accept named args nlogin (nexpose.login), page, size (int).
    Return paginated scans response.
    """
    params = {'page': page, 'size': size}
    return get(nlogin=nlogin, endpoint="api/3/scans", params=params)


def sites(*, nlogin, page=0, size=10):
    """
    Accept named args nlogin (nexpose.login), page, size (int).
    Return paginated sites response.
    """
    params = {'page': page, 'size': size}
    return get(nlogin=nlogin, endpoint="api/3/sites", params=params)


def site(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return site response.
    """
    return get(nlogin=nlogin, endpoint=f"api/3/sites/{site_id}")


def site_id_older_than(*, nlogin, site_id, days=90):
    """
    Accept named args nlogin (nexpose.login), site_id (int),
    optional days (int, default 90).
    Return True is site is older than days,
    otherwise return False
    """
    now = datetime.now()
    max_age = timedelta(days=days)
    start_dates = [
        schedule['start']
        for schedule in schedules(nlogin=nlogin, site_id=site_id)
    ]
    if len(start_dates) == 0:
        return True
    for date in start_dates:
        # Nexpose date example:
        # '2020-11-01T11:22:27Z'
        print(date)
        start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        if now - start_time < max_age:
            return False
    return True


def delete_site(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return deleted site response.
    """
    return delete(nlogin=nlogin, endpoint=f"api/3/sites/{site_id}")


def schedules(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return schedules resources.
    """
    return get(nlogin=nlogin, endpoint=f"api/3/sites/{site_id}/scan_schedules")['resources']


def assets(*, nlogin, page=0, size=10):
    """
    Accept named args nlogin (nexpose.login), page, size (int).
    Return paginated assets response.
    """
    params = {'page': page, 'size': size}
    return get(nlogin=nlogin, endpoint="api/3/assets", params=params)


def create_role(*, nlogin, role):
    """
    Accept named args nlogin (nexpose.login), role (dict).
    Return created role response.
    """
    return put(nlogin=nlogin, endpoint=f"api/3/roles/{role['id']}", data=role)
