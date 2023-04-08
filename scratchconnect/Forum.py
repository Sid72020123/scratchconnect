"""
The Forum File
"""
import requests

from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Forum:
    def __init__(self, id, client_username, headers, logged_in, online_ide):
        """
        The Main Forum Class
        :param id: The id of the forum
        """
        self.f_id = str(id)
        self.client_username = client_username
        self.headers = headers
        self._logged_in = logged_in
        if online_ide:
            _change_request_url()
        self.update_data()

    def update_data(self):
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

    def id(self):
        """
        Returns the id of the forum
        """
        return self.f_id

    def title(self):
        """
        Returns the title of the forum
        """
        return self.f_title

    def category(self):
        """
        Returns the category of the forum
        """
        return self.f_category

    def is_closed(self):
        """
        Returns whether the forum is closed or not
        """
        return self.f_is_closed

    def is_deleted(self):
        """
        Returns whether the forum is deleted or not
        """
        return self.f_is_deleted

    def time(self):
        """
        Returns the activity of the forum
        """
        return self.f_time

    def post_count(self):
        """
        Returns the total post count of the forum
        """
        return self.f_post_count

    def follow(self):
        """
        Follow a Forum
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return requests.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/add/",
                             headers=self.headers)

    def unfollow(self):
        """
        Unfollow a Forum
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return requests.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/delete/",
                             headers=self.headers)

    def posts(self, page=1):
        """
        Get the post in Forum Topic of a specified page. Images and some other stuff will not appear!
        :param page: The page
        """
        # TODO: Change the posts API
        return requests.get(f"https://scratch-forum.sid72020123.repl.co/forum/?topic={self.f_id}&page={page}").json()

    def ocular_reactions(self, post_id):
        """
        Get the ocular reactions
        :param post_id: The id of the post
        """
        return requests.get(f"https://my-ocular.jeffalo.net/api/reactions/{post_id}").json()

    def topic_post_history(self, usernames="total", segment="1", range="30"):
        """
        Get the post history of the topic
        :param usernames: Values like "total" -> Gives all the data of the users who posted in that topic, "detail" -> Gives individual user's data, or you can also put any username
        :param segment: The length of time between each segment, defaults to 1 day. Possible special cases include year(365) or month(30)
        :param range: Range of how far back to get history, defaults to 30 days. Possible special cases include year(365) or month(30)
        """
        return requests.get(
            f"https://scratchdb.lefty.one/v3/forum/topic/graph/{self.f_id}/{usernames}?segment={segment}&range={range}").json()
