"""
The Project File
"""
import json
import requests

from scratchconnect import Exceptions
from scratchconnect import CloudConnection

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"
_project = f"https://{_api}/projects/"


class Project:
    def __init__(self, id, client_username, csrf_token, session_id, token):
        """
        The Project Class
        :param id: The project ID
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
            "referer": "https://scratch.mit.edu/projects/" + self.id + "/",
        }

        self.json_headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self.session_id
                      + ";",
            "referer": "https://scratch.mit.edu/projects/" + str(self.id) + "/",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def _check(self, id):
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{id}' doesn't exist!")

    def get_author(self):
        """
        Returns the author of the project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["author"]

    def get_title(self):
        """
        Returns the title of the project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["title"]

    def get_notes(self):
        """
        Returns the notes(Notes or Credits) of the project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["description"]

    def get_instruction(self):
        """
        Returns the instructions of the project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["instructions"]

    def get_comments_allowed(self):
        """
        Returns whether the comments are allowed in a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["comments_allowed"] == True

    def get_views_count(self):
        """
        Returns the views count of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["views"]

    def get_loves_count(self):
        """
        Returns the loves count of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["loves"]

    def get_favourites_count(self):
        """
        Returns the favourites count of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["favorites"]

    def get_remixes_count(self):
        """
        Returns the remixes count of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["stats"]["remixes"]

    def get_history(self):
        """
        Returns the history of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["history"]

    def get_remix_data(self):
        """
        Returns the remix data of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["remix"]

    def get_visibility(self):
        """
        Returns whether the project is visible
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["visibility"]

    def get_is_public(self):
        """
        Returns whether the project is public
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["public"]

    def get_is_published(self):
        """
        Returns whether the project is published
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["is_published"]

    def get_thumbnail_url(self):
        """
        Returns the thumbnail url of a project
        """
        return json.loads(requests.get(f"{_project}{self.id}").text)["images"]

    def get_assets_info(self):
        """
        Returns the Assests info of a project
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/project/info/{self.id}").text)["metadata"]

    def get_scripts(self):
        """
        Returns the scripts of a project
        """
        return json.loads(requests.get(f"https://projects.scratch.mit.edu/{self.id}/").text)

    def love(self):
        """
        Love a project
        """
        return requests.post(f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self.client_username}",
                             headers=self.headers,
                             ).json()

    def unlove(self):
        """
        UnLove a project
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def favourite(self):
        """
        Favourite a project
        """
        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def unfavourite(self):
        """
        UnFavourite a project
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def get_comments(self, all=False, limit=40, offset=0, comment_id=None):
        """
        Returns the list of comments of a project
        :param all: True if you want all
        :param limit: The limit
        :param offset: The offset or the data which you want after the beginning
        :param comment_id: If you want a comment from its ID then use this
        """
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

    def post_comment(self, content, parent_id="", commentee_id=""):
        """
        Post a comment
        :param content: The comment or the content
        """
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return requests.post(
            "https://api.scratch.mit.edu/proxy/comments/project/" + str(self.id) + "/",
            headers=self.json_headers,
            data=json.dumps(data),
        )

    def toggle_commenting(self):
        """
        Toggle the commenting of a project
        """
        if self.get_author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.id}'!")
        data = {"comments_allowed": not self.get_comments_allowed()}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def turn_on_commenting(self):
        """
        Turn On the commenting of a project
        """
        if self.get_author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.id}'!")
        data = {"comments_allowed": True}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def turn_off_commenting(self):
        """
        Turn Off the commenting of a project
        """
        if self.get_author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.id}'!")
        data = {"comments_allowed": False}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def report(self, category, reason, image=None):
        """
        Report a project
        :param category: The category
        :param reason: The reason
        """
        if self.get_author()['username'] == self.client_username:
            raise Exceptions.UnauthorizedAction("You can't report your own project!")
        if not image:
            self.get_thumbnail_url()
        data = {"notes": reason, "report_category": category, "thumbnail": image}
        return requests.post(f"https://api.scratch.mit.edu/proxy/comments/project/{self.id}/",
                             data=json.dumps(data),
                             headers=self.json_headers,
                             ).text

    def unshare(self):
        """
        Unshare a project
        """
        if self.get_author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.id}'!")
        return requests.put(f"https://api.scratch.mit.edu/proxy/projects/{self.id}/unshare/",
                            headers=self.json_headers,
                            )

    def view(self):
        """
        Just view a project
        """
        return requests.post(f"https://api.scratch.mit.edu/users/{self.client_username}/projects/{self.id}/views/",
                             headers=self.headers,
                             )

    def set_thumbnail(self, file):
        """
        Set the thumbnail of a project
        :param file: The location of the file
        """
        if self.get_author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.id}'!")
        image = open(file, "rb")
        return requests.post(f"https://scratch.mit.edu/internalapi/project/thumbnail/{self.id}/set/",
                             data=image.read(),
                             headers=self.headers,
                             )

    def delete_comment(self, comment_id):
        """
        Delete a comment
        :param comment_id: Comment ID
        """
        return requests.delete(f"https://api.scratch.mit.edu/proxy/comments/project/{self.id}/comment/{comment_id}",
                               headers=self.headers,
                               )

    def report_comment(self, comment_id):
        """
        Report a comment
        :param comment_id: Comment ID
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.id}/comment/{comment_id}/report",
            headers=self.headers,
        )

    def reply_comment(self, comment_id, content):
        """
        Reply a comment
        :param comment_id: Comment ID
        :param content: The content
        """
        return self.post_comment(content=content, parent_id=comment_id)

    def set_title(self, title):
        """
        Set the title of the project
        :param title: The title
        """
        data = {'title': title}
        return requests.put(f"{_project}{self.id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_description(self, description):
        """
        Set the description of the project
        :param description: The description
        """
        data = {'description': description}
        return requests.put(f"{_project}{self.id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_instruction(self, instruction):
        """
        Set the instruction of the project
        :param instruction: The instruction
        """
        data = {'instructions': instruction}
        return requests.put(f"{_project}{self.id}", data=json.dumps(data), headers=self.json_headers).json()

    def connect_cloud_variables(self):
        """
        Connect the cloud variables of the project
        """
        return CloudConnection.CloudConnection(project_id=self.id, client_username=self.client_username,
                                               csrf_token=self.csrf_token,
                                               session_id=self.session_id, token=self.token)
