"""
The Studio File
"""
import requests
import json

import scratchconnect.ScratchConnect
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Studio:
    def __init__(self, id, client_username, csrf_token, session_id, token):
        """
        The Studio Class
        :param id: The ID of the studio
        """
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
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"{_api}/studios/{id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidStudio(f"Studio with ID - '{id}' doesn't exist!")

    def _check_project(self, project_id):
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def _check_username(self, username):
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"{_api}/users/{username}").text)["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def get_user_id(self, username):
        """
        Returns the user ID
        :param username: Username
        """
        return json.loads(requests.get(f"{_api}/users/{username}").text)["id"]

    def get_id(self):
        """
        Returns the studio ID
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["id"]

    def get_title(self):
        """
        Returns the studio title
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["title"]

    def get_owner(self):
        """
        Returns the studio owner
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["owner"]

    def get_description(self):
        """
        Returns the studio description
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["description"]

    def get_visibility(self):
        """
        Returns the studio visibility
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["visibility"]

    def get_public(self):
        """
        Returns whether a studio is public
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["public"] == True

    def get_open_to_all(self):
        """
        Returns whether a studio is open to all
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["open_to_all"] == True

    def get_comments_allowed(self):
        """
        Returns whether a studio has comments allowed
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["comments_allowed"] == True

    def get_history(self):
        """
        Returns the history of the studio
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["history"]

    def get_stats(self):
        """
        Returns the stats of the studio
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["stats"]

    def get_thumbnail_url(self):
        """
        Returns the thumbnail URL of the studio
        """
        return json.loads(requests.get(f"{_api}/studios/{self.id}/").text)["image"]

    def add_project(self, project_id):
        """
        Add a project to a studio
        :param project_id: The project ID
        """
        self._check_project(project_id)
        headers = self.headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"
        return json.loads(requests.post(f"https://api.scratch.mit.edu/studios/{self.id}/project/{project_id}/",
                                        headers=headers,
                                        ).text)

    def remove_project(self, project_id):
        """
        Remove a project from a studio
        :param project_id: The project ID
        """
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
        """
        Open the studio to public
        """
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/open/",
            headers=self.headers,
        ).text)

    def close_to_public(self):
        """
        Close the studio to public
        """
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/closed/",
            headers=self.headers,
        ).text)

    def follow_studio(self):
        """
        Follow the studio
        """
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/add/?usernames={self.client_username}",
            headers=self.headers,
        ).text)

    def unfollow_studio(self):
        """
        UnFollow the studio
        """
        return json.loads(requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/remove/?usernames={self.client_username}",
            headers=self.headers,
        ).text)

    def toggle_commenting(self):
        """
        Toggle the commenting of the studio
        """
        headers = self.headers
        headers["referer"] = (
            f"https://scratch.mit.edu/studios/{self.id}/comments/"
        )
        return requests.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/toggle-comments/",
                             headers=headers,
                             ).text

    def post_comment(self, content, parent_id="", commentee_id=""):
        """
        Post comment in the studio
        :param content: The comment
        """
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
        """
        Delete comment in the studio
        :param comment_id: The comment ID
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/comments/")
        data = {"id": comment_id}
        return requests.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/del/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def report_comment(self, comment_id):
        """
        Report comment in the studio
        :param comment_id: The comment ID
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/comments/")
        data = {"id": comment_id}
        return requests.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/rep/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def invite_curator(self, username):
        """
        Invite a user to the studio
        :param username: The Username
        """
        self._check_username(username)
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/invite_curator/?usernames={username}",
            headers=headers,
        )

    def accept_curator(self):
        """
        Accept the curator invitation in a studio
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/add/?usernames={self.client_username}",
            headers=headers,
        )

    def promote_curator(self, username):
        """
        Promote a user in the studio
        :param username: The Username
        """
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
        """
        Set the description of a Studio
        :param content: The description or content
        """
        data = {"description": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()

    def set_title(self, content):
        """
        Set the title of a Studio
        :param content: The title or content
        """
        data = {"title": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()

    def get_projects(self, all=False, limit=40, offset=0):
        """
        Get the projects of the studio
        :param all: If you want all the projects then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        projects = []
        if all:
            limit = 40
            offset = 0
            while True:
                response = json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.id}/projects/?limit={limit}&offset={offset}").text)
                projects.append(response)
                offset += 40
                if len(response) != 40:
                    break
        if not all:
            projects.append(json.loads(requests.get(
                f"https://api.scratch.mit.edu/studios/{self.id}/projects/?limit={limit}&offset={offset}").text))
        return projects
