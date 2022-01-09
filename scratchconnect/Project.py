"""
The Project File
"""
import json
import requests

from scratchconnect import Exceptions
from scratchconnect import CloudConnection
from scratchconnect import TurbowarpCloudConnection
from scratchconnect import scCloudStorage

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"
_project = f"https://{_api}/projects/"


class Project:
    def __init__(self, id, client_username, csrf_token, session_id, token, unshared):
        """
        The Project Class
        :param id: The project ID
        """
        self.access_unshared = unshared
        self.project_id = str(id)
        self.client_username = client_username
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
            "referer": "https://scratch.mit.edu/projects/" + self.project_id + "/",
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
            "referer": "https://scratch.mit.edu/projects/" + str(self.project_id) + "/",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.update_data()

    def update_data(self):
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

        data = requests.get(f"https://api.scratch.mit.edu/projects/{self.project_id}/").json()
        try:
            self.project_id = data["id"]
        except KeyError:
            if self.access_unshared:
                pass
            else:
                raise Exceptions.InvalidProject(f"The project with ID - '{self.project_id}' doesn't exist!")
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

    def id(self):
        """
        Returns the project ID
        """
        return self.project_id

    def author(self):
        """
        Returns the author of the project
        """
        if self.project_author is None:
            self.update_data()
        return self.project_author

    def title(self):
        """
        Returns the title of the project
        """
        if self.title is None:
            self.update_data()
        return self.project_title

    def notes(self):
        """
        Returns the notes(Notes or Credits) of the project
        """
        if self.project_notes is None:
            self.update_data()
        return self.project_notes

    def instructions(self):
        """
        Returns the instructions of the project
        """
        if self.project_instructions is None:
            self.update_data()
        return self.project_instructions

    def are_comments_allowed(self):
        """
        Returns whether the comments are allowed in a project
        """
        if self.project_are_comments_allowed is None:
            self.update_data()
        return self.project_are_comments_allowed

    def stats(self):
        """
        Returns the stats of a project
        """
        if self.project_stats is None:
            self.update_data()
        return self.project_stats

    def history(self):
        """
        Returns the history of a project
        """
        if self.project_history is None:
            self.update_data()
        return self.project_history

    def remix_data(self):
        """
        Returns the remix data of a project
        """
        if self.project_remix_data is None:
            self.update_data()
        return self.project_remix_data

    def visibility(self):
        """
        Returns whether the project is visible
        """
        if self.project_visibility is None:
            self.update_data()
        return self.project_visibility

    def is_public(self):
        """
        Returns whether the project is public
        """
        if self.project_is_public is None:
            self.update_data()
        return self.project_is_public

    def is_published(self):
        """
        Returns whether the project is published
        """
        if self.project_is_published is None:
            self.update_data()
        return self.project_is_public

    def thumbnail_url(self):
        """
        Returns the thumbnail url of a project
        """
        if self.project_thubmnail_url is None:
            self.update_data()
        return self.project_thubmnail_url

    def assets_info(self):
        """
        Returns the Assets info of a project
        """
        return requests.get(f"https://scratchdb.lefty.one/v3/project/info/{self.project_id}").json()[
            "metadata"]

    def scripts(self):
        """
        Returns the scripts of a project
        """
        return requests.get(f"https://projects.scratch.mit.edu/{self.project_id}/").json()

    def love(self):
        """
        Love a project
        """
        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/loves/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def unlove(self):
        """
        UnLove a project
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/loves/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def favourite(self):
        """
        Favourite a project
        """
        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def unfavourite(self):
        """
        UnFavourite a project
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/favorites/user/{self.client_username}",
            headers=self.headers,
        ).json()

    def comments(self, all=False, limit=20, offset=0, comment_id=None):
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
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{str(self.project_id)}/comments/?limit={limit}&offset={offset}"
                ).json()
                if len(response) != 40:
                    break
                offset += 40
            comments.append(response)
        if not all:
            comments.append(requests.get(
                f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{str(self.project_id)}/comments/?limit={limit}&offset={offset}"
            ).json())
        if comment_id is not None:
            comments = []
            comments.append(requests.get(
                f"https://api.scratch.mit.edu/users/{self.project_author['username']}/projects/{str(self.project_id)}/comments/{comment_id}"
            ).json())
        return comments

    def remixes(self, all=False, limit=20, offset=0):
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
                    f"https://api.scratch.mit.edu/projects/{self.project_id}/remixes/?limit=40&offset={offset}").json()
                projects += response
                if len(response) != 40:
                    break
                offset += 40
        else:
            projects.append(requests.get(
                f"https://api.scratch.mit.edu/projects/{self.project_id}/remixes/?limit={limit}&offset={offset}").json())
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
            "https://api.scratch.mit.edu/proxy/comments/project/" + str(self.project_id) + "/",
            headers=self.json_headers,
            data=json.dumps(data),
        )

    def reply_comment(self, content, comment_id):
        """
        Reply a comment
        :param content: The content
        :param comment_id: The comment ID
        """
        return self.post_comment(content=content, parent_id=comment_id)

    def toggle_commenting(self):
        """
        Toggle the commenting of a project
        """
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": not self.comments_allowed()}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def turn_on_commenting(self):
        """
        Turn On the commenting of a project
        """
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": True}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def turn_off_commenting(self):
        """
        Turn Off the commenting of a project
        """
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        data = {"comments_allowed": False}
        return requests.put(f"https://api.scratch.mit.edu/projects/{self.project_id}/",
                            data=json.dumps(data),
                            headers=self.json_headers,
                            ).json()

    def report(self, category, reason, image=None):
        """
        Report a project
        :param category: The category
        :param reason: The reason
        """
        if self.author()['username'] == self.client_username:
            raise Exceptions.UnauthorizedAction("You can't report your own project!")
        if not image:
            self.thumbnail_url()
        data = {"notes": reason, "report_category": category, "thumbnail": image}
        return requests.post(f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/",
                             data=json.dumps(data),
                             headers=self.json_headers,
                             ).text

    def unshare(self):
        """
        Unshare a project
        """
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        return requests.put(f"https://api.scratch.mit.edu/proxy/projects/{self.project_id}/unshare/",
                            headers=self.json_headers,
                            )

    def view(self):
        """
        Just view a project
        """
        return requests.post(
            f"https://api.scratch.mit.edu/users/{self.client_username}/projects/{self.project_id}/views/",
            headers=self.headers,
        )

    def set_thumbnail(self, file):
        """
        Set the thumbnail of a project
        :param file: The location of the file
        """
        if self.author()['username'] != self.client_username:
            raise Exceptions.UnauthorizedAction(
                f"You are not allowed to do that because you are not the owner of the project with ID - '{self.project_id}'!")
        image = open(file, "rb")
        return requests.post(f"https://scratch.mit.edu/internalapi/project/thumbnail/{self.project_id}/set/",
                             data=image.read(),
                             headers=self.headers,
                             )

    def delete_comment(self, comment_id):
        """
        Delete a comment
        :param comment_id: Comment ID
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/comment/{comment_id}",
            headers=self.headers,
        )

    def report_comment(self, comment_id):
        """
        Report a comment
        :param comment_id: Comment ID
        """
        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project_id}/comment/{comment_id}/report",
            headers=self.headers,
        )

    def set_title(self, title):
        """
        Set the title of the project
        :param title: The title
        """
        data = {'title': title}
        return requests.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_description(self, description):
        """
        Set the description of the project
        :param description: The description
        """
        data = {'description': description}
        return requests.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def set_instruction(self, instruction):
        """
        Set the instruction of the project
        :param instruction: The instruction
        """
        data = {'instructions': instruction}
        return requests.put(f"{_project}{self.project_id}", data=json.dumps(data), headers=self.json_headers).json()

    def connect_cloud_variables(self):
        """
        Connect the cloud variables of the project
        """
        return CloudConnection.CloudConnection(project_id=self.project_id, client_username=self.client_username,
                                               csrf_token=self.csrf_token,
                                               session_id=self.session_id, token=self.token)

    def connect_turbowarp_cloud(self, username=None):
        """
        Connect the cloud variables of the project
        """
        if username is None:
            username = self.client_username
        return TurbowarpCloudConnection.TurbowarpCloudConnection(project_id=self.project_id,
                                                                 username=username)

    def create_cloud_storage(self, file_name="data", rewrite_file=True, edit_access=None):
        """
        Create a Cloud Database in a project
        """
        if edit_access is None:
            edit_access = []
        return scCloudStorage.CloudStorage(file_name=file_name, rewrite_file=rewrite_file, project_id=self.project_id,
                                           client_username=self.client_username,
                                           csrf_token=self.csrf_token,
                                           session_id=self.session_id, token=self.token, edit_access=edit_access)
