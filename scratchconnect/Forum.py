"""
The Forum File
"""
import requests
from requests.models import Response

from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Forum:
    def __init__(self, id, client_username, headers, logged_in, online_ide, session):
        """
        The Main Forum Class
        :param id: The id of the forum
        """
        self.f_id = str(id)
        self.client_username = client_username
        self.headers = headers
        self._logged_in = logged_in
        self.session = session
        if online_ide:
            _change_request_url()
        self.update_data()

    def update_data(self) -> None:
        """
        Update the data
        """
        try:
            data = requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.f_id}").json()
        except KeyError:
            raise Exceptions.InvalidForumTopic(f"Forum with ID - '{self.f_id}' doesn't exist!")
        self.f_title = data['title']
        self.f_category = data['category']
        self.f_is_closed = data['closed'] == 1
        self.f_is_deleted = data['deleted'] == 1
        self.f_time = data['time']
        self.f_post_count = data["post_count"]

    def id(self) -> str:
        """
        Returns the id of the forum
        """
        return self.f_id

    def title(self) -> str:
        """
        Returns the title of the forum
        """
        return self.f_title

    def category(self) -> str:
        """
        Returns the category of the forum
        """
        return self.f_category

    def is_closed(self) -> bool:
        """
        Returns whether the forum is closed or not
        """
        return self.f_is_closed

    def is_deleted(self) -> bool:
        """
        Returns whether the forum is deleted or not
        """
        return self.f_is_deleted

    def time(self) -> dict:
        """
        Returns the activity of the forum
        """
        return self.f_time

    def post_count(self) -> int:
        """
        Returns the total post count of the forum
        """
        return self.f_post_count

    def follow(self) -> Response:
        """
        Follow a Forum
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return self.session.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/add/",
                                 headers=self.headers)

    def unfollow(self) -> Response:
        """
        Unfollow a Forum
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return self.session.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/delete/",
                                 headers=self.headers)

    def posts(self, page: int = 0, order: str = "newest") -> list:
        """
        Get the post in Forum Topic of a specified page. Images and some other stuff will not appear!
        :param page: The page. Default (start) value is 0
        :param order: Order to sort posts by, defaults to "newest", possible options include "oldest"
        The data os fetched from Scratch DB. So, it may not be up-to-date!
        """
        return requests.get(
            f"https://scratchdb.lefty.one/v3/forum/topic/posts/{self.id()}/{page}?o={order}").json()

    def ocular_reactions(self, post_id: int) -> dict:
        """
        Get the ocular reactions
        :param post_id: The id of the post
        """
        return requests.get(f"https://my-ocular.jeffalo.net/api/reactions/{post_id}").json()

    def topic_post_history(self, usernames: str = "total", segment: str = "1", range: str = "30") -> dict:
        """
        Get the post history of the topic
        :param usernames: Values like "total" -> Gives all the data of the users who posted in that topic, "detail" -> Gives individual user's data, or you can also put any username
        :param segment: The length of time between each segment, defaults to 1 day. Possible special cases include year(365) or month(30)
        :param range: Range of how far back to get history, defaults to 30 days. Possible special cases include year(365) or month(30)
        """
        return requests.get(
            f"https://scratchdb.lefty.one/v3/forum/topic/graph/{self.f_id}/{usernames}?segment={segment}&range={range}").json()
