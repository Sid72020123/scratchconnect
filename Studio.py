import requests
import json

import scratchconnect.Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Studio:
    def __init__(self, id, client_username, csrf_token, session_id, token):
        self.id = str(id)
        self.client_username = client_username
        self._check(self.id)
        self.csrf_token = csrf_token
        self.session_id = session_id
        self.token = token
        self.headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self.session_id
                      + ";",
            "referer": "https://scratch.mit.edu/studios/" + self.id + "/",
        }

    def _check(self, id):
        try:
            json.loads(requests.get(f"{_api}/studios/{id}/").text)["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidStudio(f"Studio with ID - '{id}' doesn't exist!")

    def get_id(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["id"]

    def get_title(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["title"]
