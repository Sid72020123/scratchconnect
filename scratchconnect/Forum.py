"""
The Forum File
"""
import requests

from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class Forum:
    def __init__(self, id, client_username, csrf_token, session_id, token):
        """
        The Main Forum Class
        :param id: The id of the forum
        """
        self.f_id = str(id)
        self.client_username = client_username
        self.update_data()
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
            "referer": "https://scratch.mit.edu/discuss/topic/" + self.f_id + "/",
        }

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
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return requests.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/add/",
                             headers=self.headers)

    def unfollow(self):
        """
        Unfollow a Forum
        """
        self.headers['referer'] = f"https://scratch.mit.edu/discuss/topic/{self.id}/"
        return requests.post(f"https://scratch.mit.edu/discuss/subscription/topic/{self.id}/delete/",
                             headers=self.headers)

    def posts(self, page=1):
        """
        Get the post in Forum Topic of a specified page. Images and some other stuff will not appear!
        :param page: The page
        """
        return requests.get(f"https://scratch-forum.sid72020123.repl.co/forum/?topic={self.f_id}&page={page}").json()
