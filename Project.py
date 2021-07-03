import json
import requests

from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"
_project = f"https://{_api}/projects/"


class Project:
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
            "referer": "https://scratch.mit.edu/projects/" + self.id + "/",
        }

    def _check(self, id):
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{id}' doesn't exist!")

    def get_project_title(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["title"]

    def get_project_notes(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["description"]

    def get_project_instruction(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["instructions"]

    def get_project_comments_allowed(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["comments_allowed"] == True

    def get_project_views(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["views"]

    def get_project_loves(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["loves"]

    def get_project_favourites(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["favorites"]

    def get_project_remixes(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["remixes"]

    def get_project_history(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["history"]

    def get_project_remix_data(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["remix"]

    def get_project_visibility(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["visibility"]

    def get_is_project_public(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["public"]

    def get_is_project_published(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["is_published"]

    def get_project_thumbnail_url(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["images"]
