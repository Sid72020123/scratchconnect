"""
Code to make it work in Online IDEs
"""

from urllib.parse import urlparse
import requests
from requests import request


def _get(url, params=None, **kwargs):
    if urlparse(url).netloc in ["api.scratch.mit.edu", "scratch.mit.edu", "cdn2.scratch.mit.edu"]:
        url = "https://scratch-proxy-test.herokuapp.com/api/" + url
    return request("get", url, params=params, **kwargs)


def _change_request_url():
    requests.get = _get
