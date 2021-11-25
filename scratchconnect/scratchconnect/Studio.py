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
        self.client_username = client_username
        self.studio_id = str(id)
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
            "referer": "https://scratch.mit.edu/studios/" + self.studio_id + "/",
        }
        self.update_data()

    def update_data(self):
        """
        Update the studio data
        """
        self.studio_title = None
        self.studio_owner = None
        self.studio_description = None
        self.studio_visibility = None
        self.studio_are_comments_allowed = None
        self.studio_history = None
        self.studio_stats = None
        self.studio_thumbnail_url = None
        self.studio_projects = None
        self.studio_comments = None
        self.studio_curators = None
        self.studio_managers = None
        self.studio_activity = None

        data = requests.get(f"{_api}/studios/{self.studio_id}/").json()
        try:
            self.studio_id = data["id"]
        except KeyError:
            raise Exceptions.InvalidStudio(f"Studio with ID - '{self.studio_id}' doesn't exist!")
        self.studio_title = data["title"]
        self.studio_owner = data["host"]
        self.studio_description = data["description"]
        self.studio_visibility = data["visibility"]
        self.studio_is_public = data["public"] == True
        self.studio_is_open_to_all = data["open_to_all"] == True
        self.studio_are_comments_allowed = data["comments_allowed"] == True
        self.studio_history = data["history"]
        self.studio_stats = data["stats"]
        self.studio_thumbnail_url = data["image"]

    def _check_project(self, project_id):
        """
        Don't use this function
        """
        try:
            requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").json()["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def _check_username(self, username):
        """
        Don't use this function
        """
        try:
            requests.get(f"{_api}/users/{username}").json()["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def user_id(self, username):
        """
        Returns the user ID
        :param username: Username
        """
        return requests.get(f"{_api}/users/{username}").json()["id"]

    def id(self):
        """
        Returns the studio ID
        """
        if self.studio_id is None:
            self.update_data()
        return self.studio_id

    def title(self):
        """
        Returns the studio title
        """
        if self.studio_title is None:
            self.update_data()
        return self.studio_title

    def host_id(self):
        """
        Returns the studio owner/host ID
        """
        if self.studio_owner is None:
            self.update_data()
        return self.studio_owner

    def description(self):
        """
        Returns the studio description
        """
        if self.studio_description is None:
            self.update_data()
        return self.studio_description

    def visibility(self):
        """
        Returns the studio visibility
        """
        if self.studio_visibility is None:
            self.update_data()
        return self.studio_visibility

    def is_public(self):
        """
        Returns whether a studio is public
        """
        if self.studio_is_public is None:
            self.update_data()
        return self.studio_is_public

    def is_open_to_all(self):
        """
        Returns whether a studio is open to all
        """
        if self.studio_is_open_to_all is None:
            self.update_data()
        return self.studio_is_open_to_all

    def are_comments_allowed(self):
        """
        Returns whether a studio has comments allowed
        """
        if self.studio_are_comments_allowed is None:
            self.update_data()
        return self.studio_are_comments_allowed

    def history(self):
        """
        Returns the history of the studio
        """
        if self.studio_history is None:
            self.update_data()
        return self.studio_history

    def stats(self):
        """
        Returns the stats of the studio
        """
        if self.studio_stats is None:
            self.update_data()
        return self.studio_stats

    def thumbnail_url(self):
        """
        Returns the thumbnail URL of the studio
        """
        if self.studio_thumbnail_url is None:
            self.update_data()
        return self.studio_thumbnail_url

    def add_project(self, project_id):
        """
        Add a project to a studio
        :param project_id: The project ID
        """
        self._check_project(project_id)
        headers = self.headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"
        return requests.post(f"https://api.scratch.mit.edu/studios/{self.studio_id}/project/{project_id}/",
                             headers=headers,
                             ).json()

    def remove_project(self, project_id):
        """
        Remove a project from a studio
        :param project_id: The project ID
        """
        self._check_project(project_id)
        headers = self.headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"
        return requests.post(
            "https://api.scratch.mit.edu/studios/"
            + str(self.studio_id)
            + "/project/"
            + str(project_id)
            + "/",
            headers=headers,
        ).json()

    def open_to_public(self):
        """
        Open the studio to public
        """
        return requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.studio_id}/mark/open/",
            headers=self.headers,
        ).json()

    def close_to_public(self):
        """
        Close the studio to public
        """
        return requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.studio_id}/mark/closed/",
            headers=self.headers,
        ).json()

    def follow_studio(self):
        """
        Follow the studio
        """
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.studio_id}/add/?usernames={self.client_username}",
            headers=self.headers,
        ).json()

    def unfollow_studio(self):
        """
        UnFollow the studio
        """
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.studio_id}/remove/?usernames={self.client_username}",
            headers=self.headers,
        ).json()

    def toggle_commenting(self):
        """
        Toggle the commenting of the studio
        """
        headers = self.headers
        headers["referer"] = (
            f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"
        )
        return requests.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.studio_id}/toggle-comments/",
                             headers=headers,
                             ).text

    def post_comment(self, content, parent_id="", commentee_id=""):
        """
        Post comment in the studio
        :param content: The comment
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"
                              )
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return requests.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.studio_id}/add/",
                             headers=headers,
                             data=json.dumps(data),
                             )

    def reply_comment(self, content, comment_id):
        """
        Reply a comment
        :param content: The content
        :param comment_id: The comment ID
        """
        return self.post_comment(content=content, parent_id=comment_id)

    def delete_comment(self, comment_id):
        """
        Delete comment in the studio
        :param comment_id: The comment ID
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.studio_id}/comments/")
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
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.studio_id}/comments/")
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
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.studio_id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/invite_curator/?usernames={username}",
            headers=headers,
        )

    def accept_curator(self):
        """
        Accept the curator invitation in a studio
        """
        headers = self.headers
        headers["referer"] = (f"https://scratch.mit.edu/studios/{self.studio_id}/curators/")
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/add/?usernames={self.client_username}",
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
                "https://scratch.mit.edu/studios/" + str(self.studio_id) + "/curators/"
        )
        return requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/promote/?usernames={username}",
            headers=headers,
        )

    def set_description(self, content):
        """
        Set the description of a Studio
        :param content: The description or content
        """
        data = {"description": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.studio_id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()

    def set_title(self, content):
        """
        Set the title of a Studio
        :param content: The title or content
        """
        data = {"title": content}
        return requests.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.studio_id}/",
                            headers=self.headers,
                            data=json.dumps(data),
                            ).json()

    def projects(self, all=False, limit=20, offset=0):
        """
        Get the projects of the studio
        :param all: If you want all the projects then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        if self.studio_projects is None:
            projects = []
            if all:
                limit = 40
                offset = 0
                while True:
                    response = json.loads(requests.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/projects/?limit={limit}&offset={offset}").text)
                    projects.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                projects.append(json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/projects/?limit={limit}&offset={offset}").text))
            self.studio_projects = projects
        return self.studio_projects

    def comments(self, all=False, limit=20, offset=0):
        """
        Get the comments of the studio
        :param all: If you want all the comments then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        if self.studio_comments is None:
            comments = []
            if all:
                limit = 40
                offset = 0
                while True:
                    response = json.loads(requests.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/comments/?limit={limit}&offset={offset}").text)
                    comments.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                comments.append(json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/comments/?limit={limit}&offset={offset}").text))
            self.studio_comments = comments
        return self.studio_comments

    def curators(self, all=False, limit=20, offset=0):
        """
        Get the curators of the studio
        :param all: If you want all the curators then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        if self.studio_curators is None:
            curators = []
            if all:
                limit = 40
                offset = 0
                while True:
                    response = json.loads(requests.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/curators/?limit={limit}&offset={offset}").text)
                    curators.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                curators.append(json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/curators/?limit={limit}&offset={offset}").text))
            self.studio_curators = curators
        return self.studio_curators

    def managers(self, all=False, limit=20, offset=0):
        """
        Get the managers of the studio
        :param all: If you want all the managers then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        if self.studio_managers is None:
            managers = []
            if all:
                limit = 40
                offset = 0
                while True:
                    response = json.loads(requests.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/managers/?limit={limit}&offset={offset}").text)
                    managers.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                managers.append(json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/managers/?limit={limit}&offset={offset}").text))
            self.studio_managers = managers
        return self.studio_managers

    def activity(self, all=False, limit=20, offset=0):
        """
        Get the activity of the studio
        :param all: If you want all the activity then set it to True
        :param limit: The limit
        :param offset: The offset or the number of data you want from the beginning
        """
        if self.studio_activity is None:
            activity = []
            if all:
                limit = 40
                offset = 0
                while True:
                    response = json.loads(requests.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/activity/?limit={limit}&offset={offset}").text)
                    activity.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                activity.append(json.loads(requests.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/activity/?limit={limit}&offset={offset}").text))
            self.studio_activity = activity
        return activity
