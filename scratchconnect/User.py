"""
The Users File
"""

from requests.models import Response
import json

from scratchconnect.UserCommon import UserCommon
from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_api = f"https://api.{_website}"


class User(UserCommon):
    def __init__(self, username, client_username, session, logged_in, online_ide):
        """
        The User Class to connect a Scratch user.
        :param username: The username
        """
        super().__init__(username, session,
                         online_ide)  # Get other properties and methods from the parent(UserCommon) class
        self.username = username
        self.client_username = client_username
        self._logged_in = logged_in
        self._user_link = f"{_api}/users/{self.username}"
        self.session = session
        if online_ide:
            _change_request_url()
        self.update_data()

    def post_comment(self, content: str, commentee_id: int = "", parent_id: int = "") -> Response:
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
        return self.session.post(f"https://scratch.mit.edu/site-api/comments/user/{self.username}/add/",
                                 data=json.dumps(data))

    def reply_comment(self, content: str, comment_id: int) -> Response:
        """
        Reply a comment
        :param content: The message
        :param comment_id: The ID of the comment you want to reply
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return self.post_comment(content=content, parent_id=comment_id)

    def report(self, field: str) -> Response:
        """
        Report an user
        :param field: The field or the reason of report.
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        if self.username == self.client_username:
            raise Exceptions.UnauthorizedAction("You are not allowed to do that!")
        data = {"selected_field": field}
        return self.session.post(f"https://scratch.mit.edu/site-api/users/all/{self.username}/report/",
                                 data=json.dumps(data))
