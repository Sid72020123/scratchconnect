import json
import requests

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"
_project = f"https://{_api}/projects/"


class Project:
    def __init__(self, project_id):
        self.project_id = project_id

    def get_project_title(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["title"]

    def get_project_notes(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["description"]

    def get_project_instruction(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["instructions"]

    def get_project_comments_allowed(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["comments_allowed"] == True

    def get_project_views(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["stats"]["views"]

    def get_project_loves(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["stats"]["loves"]

    def get_project_favourites(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["stats"]["favorites"]

    def get_project_remixes(self):
        return json.loads(requests.get(f"{_project}{self.project_id}").text)["stats"]["remixes"]
