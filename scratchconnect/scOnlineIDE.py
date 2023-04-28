"""
Code to make it work in Online IDEs
Don't use this code
"""

from urllib.parse import urlparse
import requests
from requests import request

headers = {"library": "ScratchConnect.py"}
scratch_endpoints = ["api.scratch.mit.edu", "scratch.mit.edu", "cdn2.scratch.mit.edu"]

proxy_url = "https://apis.scratchconnect.eu.org/proxy/get?url="


def _get(url, params=None, **kwargs):
    if urlparse(url).netloc in scratch_endpoints:
        url = proxy_url + url
        kwargs["headers"] = headers
    return request("GET", url, params=params, **kwargs)


def _session_get(self, url, **kwargs):
    if urlparse(url).netloc in scratch_endpoints:
        url = proxy_url + url
        kwargs["headers"] = headers
    return request("GET", url, **kwargs)


def _change_request_url():
    requests.get = _get
    requests.Session.get = _session_get
