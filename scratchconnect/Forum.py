"""
The Forum File
"""
import requests
import json

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
            "referer": "https://scratch.mit.edu/discuss/topic/" + self.id + "/",
        }

    def _check(self, id):
        """
        Don't use this
        """
        try:
            json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{id}").text)["id"]
        except KeyError:
            raise Exceptions.InvalidStudio(f"Forum with ID - '{id}' doesn't exist!")

    def get_id(self):
        """
        Returns the id of the forum
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)["id"]

    def get_title(self):
        """
        Returns the title of the forum
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)["title"]

    def get_category(self):
        """
        Returns the category of the forum
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)["category"]

    def get_closed(self):
        """
        Returns whether the forum is closed or not
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)[
                   "closed"] == 1

    def get_deleted(self):
        """
        Returns whether the forum is deleted or not
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)[
                   "deleted"] == 1

    def get_time(self):
        """
        Returns the activity of the forum
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)["time"]

    def get_post_count(self):
        """
        Returns the total post count of the forum
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}").text)["post_count"]

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
