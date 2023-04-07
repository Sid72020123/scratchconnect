"""
The Project File
"""
import json

import requests
from requests.models import Response

from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import CloudConnection
from scratchconnect import TurbowarpCloudConnection
from scratchconnect import scCloudRequests
from scratchconnect import Exceptions
from scratchconnect import Warnings

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"
_project = f"https://{_api}/projects/"


class Project:
    def __init__(self, id, client_username, session, unshared, logged_in, session_id, online_ide):
        """
        The Project Class
        :param id: The project ID
        """
        self.access_unshared = unshared
        self.project_id = str(id)
        self.client_username = client_username
        self.session = session
        self.csrf_token = self.session.headers["x-csrftoken"]
        self.session_id = session_id
        self.token = self.session.headers["X-Token"]
        self._logged_in = logged_in
        self.json_headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};",
            "referer": f"https://scratch.mit.edu/projects/{self.project_id}/",
            "accept": "application/json",
            "Content-Type": "application/json",
            "origin": f"https://{_website}"
        }
        if online_ide:
            _change_request_url()
        self.online_ide = online_ide
        self.update_data()

    def update_data(self) -> None:
        self.project_author = None
        self.project_title = None
        self.project_notes = None
        self.project_instructions = None
        self.project_are_comments_allowed = None
        self.project_stats = None
        self.project_history = None
        self.project_remix_data = None
        self.project_visibility = None
        self.project_is_public = None
        self.project_is_published = None
        self.project_thubmnail_url = None
        self.project_token = None

        data = self.session.get(f"{_project}{self.project_id}").json()
        try:
            self.project_id = data["id"]
        except KeyError:
            if self.access_unshared:
                pass
            else:
                raise Exceptions.InvalidProject(
                    f"The project with ID - '{self.project_id}' doesn't exist or is unshared! To connect an unshared project using ScratchConnect, use the access_unshared parameter of the Project class.")
        if not self.access_unshared:
            self.project_author = data["author"]
            self.project_title = data["title"]
            self.project_notes = data["description"]
            self.project_instructions = data["instructions"]
            self.project_are_comments_allowed = data["comments_allowed"] == True
            self.project_stats = data["stats"]
            self.project_history = data["history"]
            self.project_remix_data = data["remix"]
            self.project_visibility = data["visibility"]
            self.project_is_public = data["public"] == True
            self.project_is_published = data["is_published"] == True
            self.project_thubmnail_url = data["images"]
            self.project_token = data["project_token"]

    def id(self) -> int:
        """
        Returns the project ID
        """
        return self.project_id

    def author(self) -> dict:
        """
        Returns the author of the project
        """
        if self.project_author is None:
            self.update_data()
        return self.project_author

    def title(self) -> str:
        """
        Returns the title of the project
        """
        if self.title is None:
            self.update_data()
        return self.project_title

    def notes(self) -> str:
        """
        Returns the notes(Notes or Credits) of the project
        """
        if self.project_notes is None:
            self.update_data()
        return self.project_notes

    def instructions(self) -> str:
        """
        Returns the instructions of the project
        """
        if self.project_instructions is None:
            self.update_data()
        return self.project_instructions

    def are_comments_allowed(self) -> bool:
        """
        Returns whether the comments are allowed in a project
        """
        if self.project_are_comments_allowed is None:
            self.update_data()
        return self.project_are_comments_allowed

    def stats(self) -> dict:
        """
        Returns the stats of a project
        """
        if self.project_stats is None:
            self.update_data()
        return self.project_stats

    def history(self) -> dict:
        """
        Returns the history of a project
        """
        if self.project_history is None:
            self.update_data()
        return self.project_history

    def remix_data(self) -> dict:
        """
        Returns the remix data of a project
        """
        if self.project_remix_data is None:
            self.update_data()
        return self.project_remix_data

    def visibility(self) -> str:
        """
        Returns whether the project is visible
        """
        if self.project_visibility is None:
            self.update_data()
        return self.project_visibility

    def is_public(self) -> bool:
        """
        Returns whether the project is public
        """
        if self.project_is_public is None:
            self.update_data()
        return self.project_is_public

    def is_published(self) -> bool:
        """
        Returns whether the project is published
        """
        if self.project_is_published is None:
            self.update_data()
        return self.project_is_public

    def thumbnail_url(self) -> dict:
        """
        Returns the thumbnail url of a project
        """
        if self.project_thubmnail_url is None:
            self.update_data()
        return self.project_thubmnail_url

    def assets_info(self) -> dict:
        """
        Returns the Assets info of a project
        """
        return requests.get(f"https://scratchdb.lefty.one/v3/project/info/{self.project_id}").json()[
            "metadata"]

    def scripts(self) -> dict:
        """
        Returns the scripts of a project
        """
        return self.session.get(f"https://projects.scratch.mit.edu/{self.project_id}?token={self.project_token}").json()

    def love(self) -> dict:
        """
        Love a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/loves/user/{self.client_username}").json()

    def unlove(self) -> dict:
        """
        UnLove a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/loves/user/{self.client_username}").json()

    def favourite(self) -> dict:
        """
        Favourite a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/favorites/user/{self.client_username}").json()

    def unfavourite(self):
        """
        UnFavourite a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/favorites/user/{self.client_username}").json()

    def comments(self, all: bool = False, limit: int = 20, offset: int = 0, comment_id: int = None) -> list:
        """
        Returns the list of comments of a project
        :param all: True if you want all
        :param limit: The limit
        :param offset: The offset or the data which you want after the beginning
        :param comment_id: If you want a comment from its ID then use this
        """
        if self.project_author is None:
            self.update_data()
        comments = []
        if all:
            offset = 40
            limit = 40
            while True:
                response = self.session.get(
                    f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{self.project_id}/comments/?limit={limit}&offset={offset}").json()
                if len(response) != 40:
                    break
                offset += 40
            comments.append(response)
        if not all:
            comments.append(self.session.get(
                f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{self.project_id}/comments/?limit={limit}&offset={offset}"
            ).json())
        if comment_id is not None:
            comments = []
            comments.append(self.session.get(
                f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{self.project_id}/comments/{comment_id}"
            ).json())
        return comments

    def remixes(self, all: bool = False, limit: int = 20, offset: int = 0) -> list:
        """
        Returns the list of remixes of a project
        :param all: True if you want all
        :param limit: The limit
        :param offset: The offset or the data which you want after the beginning
        """
        projects = []
        if all:
            offset = 0
            while True:
                response = self.session.get(
                    f"https://api.scratch.mit.edu/projects/{self.project_id}/remixes/?limit=40&offset={offset}").json()
                projects += response
                if len(response) != 40:
                    break
                offset += 40
        else:
            projects.append(self.session.get(
                f"https://api.scratch.mit.edu/projects/{self.project_id}/remixes/?limit={limit}&offset={offset}").json())
        return projects

    def post_comment(self, content: str, parent_id: int = "", commentee_id: int = "") -> Response:
        """
        Post a comment
        :param content: The comment or the content
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return self.session.post(f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/",
                                 data=json.dumps(data), headers=self.json_headers)

    def reply_comment(self, content: str, comment_id: int) -> Response:
        """
        Reply a comment
        :param content: The content
        :param comment_id: The comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.post_comment(content=content, parent_id=comment_id)

    def toggle_commenting(self) -> dict:
        """
        Toggle the commenting of a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": not self.are_comments_allowed()}
        return self.session.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/", data=json.dumps(data),
                                headers=self.json_headers).json()

    def turn_on_commenting(self) -> dict:
        """
        Turn On the commenting of a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": True}
        return self.session.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/", data=json.dumps(data),
                                headers=self.json_headers).json()

    def turn_off_commenting(self) -> dict:
        """
        Turn Off the commenting of a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": False}
        return self.session.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/", data=json.dumps(data),
                                headers=self.json_headers, ).json()

    def report(self, category: str, reason: str, image: str = None) -> str:
        """
        Report a project
        :param category: The category
        :param reason: The reason
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] == self.client_username:
            raise Exceptions.UnauthorizedAction("You can't report your own project!")
        if not image:
            image = self.thumbnail_url()
        data = {"notes": reason, "report_category": category, "thumbnail": image}
        return self.session.post(f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/",
                                 data=json.dumps(data), headers=self.json_headers).text

    def unshare(self) -> Response:
        """
        Unshare a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        return self.session.put(f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/unshare/",
                                headers=self.json_headers)

    def share(self) -> Response:
        """
        Share a project
        """
        Warnings.warn(
            "[1m[33mScratchConnect Warning: [31mThe 'share()' function doesn't work sometimes because the Scratch server blocks the request returning the status code 503.[0m")
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.put(f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/share/",
                                headers=self.json_headers)

    def view(self) -> Response:
        """
        Just view a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.post(
            f"https://api.scratch.mit.edu/users/{self.client_username}/projects/{self.project_id}/views/")

    def set_thumbnail(self, file: str) -> Response:
        """
        Set the thumbnail of a project
        :param file: The location of the file
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        with open(file, "rb") as f:
            image = f.read()
        return self.session.post(f"https://scratch.mit.edu/internalapi/project/thumbnail/{self.project_id}/set/",
                                 data=image)

    def delete_comment(self, comment_id: int) -> Response:
        """
        Delete a comment
        :param comment_id: Comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/comment/{comment_id}")

    def report_comment(self, comment_id: int) -> Response:
        """
        Report a comment
        :param comment_id: Comment ID
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.session.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/comment/{comment_id}/report")

    def set_title(self, title: str) -> dict:
        """
        Set the title of the project
        :param title: The title
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {'title': title}
        return self.session.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_description(self, description: str) -> dict:
        """
        Set the description of the project
        :param description: The description
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {'description': description}
        return self.session.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_instruction(self, instruction: str) -> dict:
        """
        Set the instruction of the project
        :param instruction: The instruction
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {'instructions': instruction}
        return self.session.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def remix_project(self, title: str) -> dict:
        """
        Remix the project
        :param title: The title of the remixed project
        """
        Warnings.warn(
            "[1m[33mScratchConnect Warning: [31mThe 'remix_project()' function doesn't work sometimes because the Scratch server blocks the request returning the status code 503.[0m")
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.access_unshared:
            raise Exceptions.UnauthorizedAction(
                "Cannot perform the action because the project as is accessed as an unshared project.")
        return self.session.post(
            f"https://projects.scratch.mit.edu/?is_remix=1&original_id={self.id()}&title={title}",
            data=json.dumps(self.scripts()), headers={"origin": f"https://{_website}"})

    def connect_cloud_variables(self) -> CloudConnection.CloudConnection:
        """
        Connect the cloud variables of the project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return CloudConnection.CloudConnection(project_id=self.project_id, client_username=self.client_username,
                                               csrf_token=self.csrf_token,
                                               session_id=self.session_id, token=self.token, session=self.session,
                                               online_ide=self.online_ide)

    def connect_turbowarp_cloud(self, username: str = None) -> TurbowarpCloudConnection.TurbowarpCloudConnection:
        """
        Connect the cloud variables of the project
        """
        if username is None:
            username = self.client_username
        return TurbowarpCloudConnection.TurbowarpCloudConnection(project_id=self.project_id,
                                                                 username=username)

    def create_cloud_storage(self):
        """
        Create a Cloud Database/Storage in a project
        """
        Warnings.warn(
            "[1m[33mScratchConnect Warning: [31mThe Cloud Storage feature is deprecated since the v5.0 of the library. Please use the new alternative Cloud Requests feature instead![0m")

    def create_cloud_requests(self, handle_all_errors: bool = True,
                              print_logs: bool = True) -> scCloudRequests.CloudRequests:
        """
        Create a Cloud Database/Storage in a project
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return scCloudRequests.CloudRequests(project_id=self.project_id,
                                             client_username=self.client_username,
                                             csrf_token=self.csrf_token,
                                             session_id=self.session_id, token=self.token,
                                             handle_all_errors=handle_all_errors, print_logs=print_logs,
                                             session=self.session, online_ide=self.online_ide)

    def all_data(self) -> dict:
        """
        Returns all the data of a Scratch Project
        """
        data = {
            'Project ID': self.id(),
            'Project Name': self.title(),
            'Author': self.author()['username'],
            'Are Comments Allowed?': self.are_comments_allowed(),
            'Views': self.stats()['views'],
            'Loves': self.stats()['loves'],
            'Favourites': self.stats()['favorites'],
            'Remixes': self.stats()['remixes'],
            'Visibility': self.visibility(),
            'Is public?': self.is_public(),
            'Is published?': self.is_published(),
            'Version': self.assets_info()['version'],
            'Costumes': self.assets_info()['costumes'],
            'Blocks': self.assets_info()['blocks'],
            'Variables': self.assets_info()['variables'],
            'Assets': self.assets_info()['assets']
        }
        return data
