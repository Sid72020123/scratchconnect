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

    def get_author(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["author"]

    def get_title(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["title"]

    def get_notes(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["description"]

    def get_instruction(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["instructions"]

    def get_comments_allowed(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["comments_allowed"] == True

    def get_views(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["views"]

    def get_loves(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["loves"]

    def get_favourites(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["favorites"]

    def get_remixes(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["remixes"]

    def get_history(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["history"]

    def get_remix_data(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["remix"]

    def get_visibility(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["visibility"]

    def get_is_public(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["public"]

    def get_is_published(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["is_published"]

    def get_thumbnail_url(self):
        return json.loads(requests.get(f"{_project}{self.id}").text)["images"]

    def get_assets_info(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/project/info/{self.id}").text)["metadata"]

    def get_scripts(self):
        return json.loads(requests.get(f"https://projects.scratch.mit.edu/{self.id}/").text)

    def love(self):
        return requests.post(f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self.client_username}",
                             headers=self.headers,
                             ).json()

    def unlove(self):
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def favourite(self):
        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def unfavourite(self):
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def get_comments(self, all=False, limit=40, offset=0, comment_id=None):
        comments = []
        if all:
            offset = 40
            limit = 40
            while True:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.get_author()['username']}/projects/{str(self.id)}/comments/?limit={limit}&offset={offset}"
                ).json()
                if len(response) != 40:
                    break
                offset += 40
            comments.append(response)
        if not all:
            comments.append(requests.get(
                f"https://api.scratch.mit.edu/users/{self.get_author()['username']}/projects/{str(self.id)}/comments/?limit={limit}&offset={offset}"
            ).json())
        if comment_id is not None:
            comments = []
            comments.append(requests.get(
                f"https://api.scratch.mit.edu/users/{self.get_author()['username']}/projects/{str(self.id)}/comments/{comment_id}"
            ).json())
        return comments

    def get_remixes(self, all=False, limit=20, offset=0):
        projects = []
        if all:
            offset = 0
            while True:
                response = requests.get(
                    f"https://api.scratch.mit.edu/projects/{self.id}/remixes/?limit=40&offset={offset}").json()
                projects += response
                if len(response) != 40:
                    break
                offset += 40
        else:
            projects.append(requests.get(
                f"https://api.scratch.mit.edu/projects/{self.id}/remixes/?limit={limit}&offset={offset}").json())
        return projects
