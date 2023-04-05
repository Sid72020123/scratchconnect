"""
The Studio File
"""
import requests
from requests.models import Response
import json

import scratchconnect.ScratchConnect
from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Studio:
    def __init__(self, id, client_username, session, logged_in, online_ide):
        """
        The Studio Class
        :param id: The ID of the studio
        """
        self.client_username = client_username
        self._logged_in = logged_in
        self.studio_id = str(id)
        self.session = session
        if online_ide:
            _change_request_url()
        self.update_data()

    def update_data(self) -> None:
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

        data = self.session.get(f"{_api}/studios/{self.studio_id}").json()
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

    def _check_project(self, project_id: int) -> None:
        """
        Don't use this function
        """
        try:
            requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").json()["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def _check_username(self, username) -> None:
        """
        Don't use this function
        """
        try:
            requests.get(f"{_api}/users/{username}").json()["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def user_id(self, username) -> int:
        """
        Returns the user ID
        :param username: Username
        """
        return self.session.get(f"{_api}/users/{username}").json()["id"]

    def id(self) -> int:
        """
        Returns the studio ID
        """
        if self.studio_id is None:
            self.update_data()
        return self.studio_id

    def title(self) -> str:
        """
        Returns the studio title
        """
        if self.studio_title is None:
            self.update_data()
        return self.studio_title

    def host_id(self) -> int:
        """
        Returns the studio owner/host ID
        """
        if self.studio_owner is None:
            self.update_data()
        return self.studio_owner

    def description(self) -> str:
        """
        Returns the studio description
        """
        if self.studio_description is None:
            self.update_data()
        return self.studio_description

    def visibility(self) -> str:
        """
        Returns the studio visibility
        """
        if self.studio_visibility is None:
            self.update_data()
        return self.studio_visibility

    def is_public(self) -> bool:
        """
        Returns whether a studio is public
        """
        if self.studio_is_public is None:
            self.update_data()
        return self.studio_is_public

    def is_open_to_all(self) -> bool:
        """
        Returns whether a studio is open to all
        """
        if self.studio_is_open_to_all is None:
            self.update_data()
        return self.studio_is_open_to_all

    def are_comments_allowed(self) -> bool:
        """
        Returns whether a studio has comments allowed
        """
        if self.studio_are_comments_allowed is None:
            self.update_data()
        return self.studio_are_comments_allowed

    def history(self) -> dict:
        """
        Returns the history of the studio
        """
        if self.studio_history is None:
            self.update_data()
        return self.studio_history

    def stats(self) -> dict:
        """
        Returns the stats of the studio
        """
        if self.studio_stats is None:
            self.update_data()
        return self.studio_stats

    def thumbnail_url(self) -> str:
        """
        Returns the thumbnail URL of the studio
        """
        if self.studio_thumbnail_url is None:
            self.update_data()
        return self.studio_thumbnail_url

    def add_project(self, project_id) -> dict:
        """
        Add a project to a studio
        :param project_id: The project ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self._check_project(project_id)
        headers = {"referer": f"https://scratch.mit.edu/projects/{project_id}/"}
        return self.session.post(f"https://api.scratch.mit.edu/studios/{self.studio_id}/project/{project_id}/",
                                 headers=headers).json()

    def remove_project(self, project_id) -> dict:
        """
        Remove a project from a studio
        :param project_id: The project ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self._check_project(project_id)
        headers = {"referer": f"https://scratch.mit.edu/projects/{project_id}/"}
        return self.session.post(f"https://api.scratch.mit.edu/studios/{self.studio_id}/project/{project_id}/",
                                 headers=headers).json()

    def open_to_public(self) -> dict:
        """
        Open the studio to public
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.studio_id}/mark/open/").json()

    def close_to_public(self) -> dict:
        """
        Close the studio to public
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.studio_id}/mark/closed/").json()

    def follow_studio(self) -> dict:
        """
        Follow the studio
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.studio_id}/add/?usernames={self.client_username}").json()

    def unfollow_studio(self) -> dict:
        """
        UnFollow the studio
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.studio_id}/remove/?usernames={self.client_username}").json()

    def toggle_commenting(self) -> str:
        """
        Toggle the commenting of the studio
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"}
        return self.session.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.studio_id}/toggle-comments/",
                                 headers=headers).text

    def post_comment(self, content: str, parent_id: int = "", commentee_id: int = "") -> Response:
        """
        Post comment in the studio
        :param content: The comment
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"}
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return self.session.post(f"https://scratch.mit.edu/site-api/comments/gallery/{self.studio_id}/add/",
                                 headers=headers,
                                 data=json.dumps(data)
                                 )

    def reply_comment(self, content: str, comment_id: int) -> Response:
        """
        Reply a comment
        :param content: The content
        :param comment_id: The comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.post_comment(content=content, parent_id=comment_id)

    def delete_comment(self, comment_id: int) -> Response:
        """
        Delete comment in the studio
        :param comment_id: The comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"}
        data = {"id": comment_id}
        return self.session.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/del/",
                                 headers=headers, data=json.dumps(data))

    def report_comment(self, comment_id: int) -> Response:
        """
        Report comment in the studio
        :param comment_id: The comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/comments/"}
        data = {"id": comment_id}
        return self.session.post(f"https://scratch.mit.edu/site-api/comments/user/{self.client_username}/rep/",
                                 headers=headers, data=json.dumps(data))

    def invite_curator(self, username: str) -> Response:
        """
        Invite a user to the studio
        :param username: The Username
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self._check_username(username)
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/curators/"}
        return self.session.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/invite_curator/?usernames={username}",
            headers=headers)

    def accept_curator(self) -> Response:
        """
        Accept the curator invitation in a studio
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        headers = {"referer": f"https://scratch.mit.edu/studios/{self.studio_id}/curators/"}
        return self.session.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/add/?usernames={self.client_username}",
            headers=headers)

    def promote_curator(self, username: str) -> Response:
        """
        Promote a user in the studio
        :param username: The Username
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self._check_username(username)
        headers = {"referer": "https://scratch.mit.edu/studios/" + str(self.studio_id) + "/curators/"}
        return self.session.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.studio_id}/promote/?usernames={username}",
            headers=headers)

    def set_description(self, content: str) -> dict:
        """
        Set the description of a Studio
        :param content: The description or content
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {"description": content}
        return self.session.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.studio_id}/",
                                data=json.dumps(data)).json()

    def set_title(self, content: str) -> dict:
        """
        Set the title of a Studio
        :param content: The title or content
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {"title": content}
        return self.session.put(f"https://scratch.mit.edu/site-api/galleries/all/{self.studio_id}/",
                                data=json.dumps(data)).json()

    def projects(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
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
                    response = self.session.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/projects/?limit={limit}&offset={offset}").json()
                    projects.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                projects.append(self.session.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/projects/?limit={limit}&offset={offset}").json())
            self.studio_projects = projects
        return self.studio_projects

    def comments(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
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
                    response = self.session.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/comments/?limit={limit}&offset={offset}").json()
                    comments.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                comments.append(self.session.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/comments/?limit={limit}&offset={offset}").json())
            self.studio_comments = comments
        return self.studio_comments

    def curators(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
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
                    response = self.session.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/curators/?limit={limit}&offset={offset}").json()
                    curators.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                curators.append(self.session.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/curators/?limit={limit}&offset={offset}").json())
            self.studio_curators = curators
        return self.studio_curators

    def managers(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
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
                    response = self.session.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/managers/?limit={limit}&offset={offset}").json()
                    managers.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                managers.append(self.session.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/managers/?limit={limit}&offset={offset}").json())
            self.studio_managers = managers
        return self.studio_managers

    def activity(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
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
                    response = self.session.get(
                        f"https://api.scratch.mit.edu/studios/{self.studio_id}/activity/?limit={limit}&offset={offset}").json()
                    activity.append(response)
                    offset += 40
                    if len(response) != 40:
                        break
            if not all:
                activity.append(self.session.get(
                    f"https://api.scratch.mit.edu/studios/{self.studio_id}/activity/?limit={limit}&offset={offset}").json())
            self.studio_activity = activity
        return self.studio_activity

    def all_data(self) -> dict:
        """
        Returns all the data of a Scratch Studio
        """
        data = {
            'Studio ID': self.id(),
            'Title': self.title(),
            'Host ID': self.host_id(),
            'Description': self.description(),
            'Comments Count': self.stats()['comments'],
            'Followers Count': self.stats()['followers'],
            'Managers Count': self.stats()['managers'],
            'Projects Count': self.stats()['projects'],
            'Visibility': self.visibility(),
            'Is Public?': self.is_public(),
            'Is Open To All?': self.is_open_to_all(),
            'Are Comments Allowed?': self.are_comments_allowed(),
        }
        return data
