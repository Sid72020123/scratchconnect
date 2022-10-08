"""
The Users File
"""
import requests
import json

from scratchconnect.UserCommon import UserCommon
from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class User(UserCommon):
    def __init__(self, username, client_username, headers, logged_in, online_ide):
        """
        The User Class to connect a Scratch user.
        :param username: The username
        """
        super().__init__(username, headers, online_ide)  # Get other properties and methods from the parent(UserCommon) class
        self.username = username
        self.client_username = client_username
        self._logged_in = logged_in
        self._user_link = f"{_api}/users/{self.username}"
        self.headers = headers
        if online_ide:
            _change_request_url()
        self.update_data()

    def post_comment(self, content, commentee_id="", parent_id=""):
        """
        Post a comment on the user's profile
        :param content: The comment
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return requests.post(
            f"https://scratch.mit.edu/site-api/comments/user/{self.username}/add/",
            headers=self.headers,
            data=json.dumps(data),
        )

    def reply_comment(self, content, comment_id):
        """
        Reply a comment
        :param content: The message
        :param comment_id: The ID of the comment you want to reply
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.post_comment(content=content, parent_id=comment_id)

    def report(self, field):
        """
        Report an user
        :param field: The field or the reason of report.
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.username == self.client_username:
            raise Exceptions.UnauthorizedAction("You are not allowed to do that!")
        data = {"selected_field": field}
        requests.post(f"https://scratch.mit.edu/site-api/users/all/{self.username}/report/",
                      headers=self.headers,
                      data=json.dumps(data),
                      )
