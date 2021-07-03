import requests
import json

import scratchconnect.ScratchConnect
from scratchconnect import Exceptions

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

    def _check_project(self, project_id):
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def _check_username(self, username):
        try:
            json.loads(requests.get(f"{_api}/users/{username}").text)["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def get_user_id(self, username):
        return json.loads(requests.get(f"{_api}/users/{username}").text)["id"]

    def get_id(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["id"]

    def get_title(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["title"]

    def get_owner(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["owner"]

    def get_description(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["description"]

    def get_visibility(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["visibility"]

    def get_public(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["public"] == True

    def get_open_to_all(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["open_to_all"] == True

    def get_comments_allowed(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["comments_allowed"] == True

    def get_history(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["history"]

    def get_stats(self):
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["stats"]

    def add_project(self, project_id):
        self._check_project(project_id)
        if not (self.get_owner() == self.get_user_id(self.client_username) and self.get_open_to_all()):
            raise Exceptions.UnauthorizedAction(
                f"The owner of the studio ID - '{self.id}' has forbidden to allow add projects to non-curators!")
        headers = self.headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"
        return json.loads(requests.post(
            "https://api.scratch.mit.edu/studios/"
            + str(self.id)
            + "/project/"
            + str(project_id)
            + "/",
            headers=headers,
        ).text)

    def remove_project(self, project_id):
        self._check_project(project_id)
        headers = self.headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"
        return json.loads(requests.post(
            "https://api.scratch.mit.edu/studios/"
            + str(self.id)
            + "/project/"
            + str(project_id)
            + "/",
            headers=headers,
        ).text)

    def open_to_public(self):
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/open/",
            headers=self.headers,
        ).text)

    def close_to_public(self):
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/closed/",
            headers=self.headers,
        ).text)

    def follow_studio(self):
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/add/?usernames={self.client_username}",
            headers=self.headers,
        ).text)

    def unfollow_studio(self):
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/remove/?usernames={self.client_username}",
            headers=self.headers,
        ).text)

    def toggle_commenting(self):
        headers = self.headers
        headers["referer"] = (
            f"https://scratch.mit.edu/studios/{self.id}/comments/"
        )
        return requests.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/toggle-comments/",
                             headers=headers,
                             ).text

    def post_comment(self, content, parent_id="", commentee_id=""):
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/comments/"
                              )
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return requests.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/add/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def delete_comment(self, comment_id):
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/comments/")
        data = {"id": comment_id}
        return requests.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/del/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def report_comment(self, comment_id):
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/comments/")
        data = {"id": comment_id}
        return requests.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/rep/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def invite_curator(self, username):
        self._check_username(username)
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/invite_curator/?usernames={username}",
            headers=headers,
        )

    def accept_curator(self):
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/add/?usernames={self.client_username}",
            headers=headers,
        )

    def promote_curator(self, username):
        self._check_username(username)
        headers = self.headers
        headers["referer"] = (
                "https://scratch.mit.edu/studios/" + str(self.id) + "/curators/"
        )
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/promote/?usernames={username}",
            headers=headers,
        )

    def set_description(self, content):
        data = {"description": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()

    def set_title(self, content):
        data = {"title": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()
