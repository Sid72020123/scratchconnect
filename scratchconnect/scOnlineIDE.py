"""
Code to make it work in Online IDEs
Don't use this code
"""

from urllib.parse import urlparse
import requests
from requests import request

headers = {"Library": "ScratchConnect.py"}


def _get(url, params=None, **kwargs):
    if urlparse(url).netloc in ["api.scratch.mit.edu", "scratch.mit.edu", "cdn2.scratch.mit.edu"]:
        url = "https://sc-proxy.scratchconnect.eu.org/get/" + url
    return request("get", url, headers=headers, params=params, **kwargs)


def _change_request_url():
    requests.get = _get
