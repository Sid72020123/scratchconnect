"""
The Users File
"""
import requests
import json

from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class User:
    def __init__(self, username, client_username, csrf_token, session_id, token):
        """
        The User Class to connect a Scratch user.
        :param username: The username
        """
        self.username = username
        self.client_username = client_username
        self._check(self.username)
        self._user_link = f"{_api}/users/{self.username}"
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
            "referer": "https://scratch.mit.edu/users/" + self.username + "/",
        }

    def _check(self, username):
        """
        Don't use this.
        """
        try:
            json.loads(requests.get(f"{_api}/users/{username}").text)["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{self.username}' doesn't exist!")

    def get_id(self, username=None):
        """
        Get the ID of a user's profile
        :param username: The username
        """
        if username is None:
            username = self.username
        return json.loads(requests.get(f"{_api}/users/{username}").text)["id"]

    def get_messages_count(self):
        """
        Get the messages count of the user
        """
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
        return json.loads(requests.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count", headers=headers).text)[
            "count"]

    def get_work(self):
        """
        Returns the 'What I am working on' of a Scratch profile
        """
        return json.loads(requests.get(self._user_link).text)["profile"]["status"]

    def get_bio(self):
        """
        Returns the 'About me' of a Scratch profile
        """
        return json.loads(requests.get(self._user_link).text)["profile"]["bio"]

    def get_status(self):
        """
        Returns the status(Scratcher or New Scratcher) of a Scratch profile
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["status"]

    def get_joined_date(self):
        """
        Returns the joined date of a Scratch profile
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["joined"]

    def get_country(self):
        """
        Returns the country of a Scratch profile
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["country"]

    def get_follower_count(self):
        """
        Returns the follower count of a user
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "followers"]

    def get_following_count(self):
        """
        Returns the following count of a user
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "following"]

    def get_total_views(self):
        """
        Returns the total views count of all the shared projects of a user
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "views"]

    def get_total_loves(self):
        """
        Returns the total loves count of all the shared projects of a user
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "loves"]

    def get_total_favourites(self):
        """
        Returns the total favourites count of all the shared projects of a user
        """
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "favorites"]

    def get_featured_data(self):
        """
        Returns the featured project data of the Scratch profile
        """
        return json.loads(requests.get(f"https://scratch.mit.edu/site-api/users/all/{self.username}").text)

    def get_projects(self, all=False, limit=20, offset=0):
        """
        Returns the list of shared projects of a user
        :param all: If you want all then set it to True
        :param limit: The limit of the projects
        :param offset: The number of projects to be skipped from the beginning
        """
        if all:
            projects = []
            offset = 0
            while True:
                request = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit=40&offset={offset}").text
                projects.append(request)
                if len(request) != 40:
                    break
                offset += 40
        if not all:
            projects = []
            for i in range(1, limit + 1):
                request = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit={limit}&offset={offset}").text
                projects.append(request)
        return projects

    def get_following(self, all=False, limit=40, offset=0):
        """
        Returns the list of the user following
        :param all: If you want all then set it to True
        :param limit: The limit of the users
        :param offset: The number of users to be skipped from the beginning
        """
        following = []
        if all:
            offset = 0
            while True:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/following/?limit=40&offset={offset}").text
                offset += 40
                following.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/following/?limit={limit}&offset={offset}").text
            following.append(response)
        return following

    def get_followers(self, all=False, limit=40, offset=0):
        """
        Returns the list of the user followers
        :param all: If you want all then set it to True
        :param limit: The limit of the users
        :param offset: The number of users to be skipped from the beginning
        """
        followers = []
        if all:
            offset = 0
            while True:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit=40&offset={offset}").text
                offset += 40
                followers.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit={limit}&offset={offset}").text
            followers.append(response)
        return followers

    def get_favourites(self, all=False, limit=40, offset=0):
        """
        Returns the list of the user favourites
        :param all: If you want all then set it to True
        :param limit: The limit of the projects
        :param offset: The number of projects to be skipped from the beginning
        """
        favorites = []
        if all:
            offset = 0
            while True:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit=40&offset={offset}").text
                offset += 40
                favorites.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit={limit}&offset={offset}").text
            favorites.append(response)
        return favorites

    def get_user_follower_history(self, segment="", range=30):
        """
        Return the follower history of the user
        :param segment: The length of time between each segment, defaults to 1 day.
        :param range: Of how far back to get history, defaults to 30 days
        """
        return json.loads(requests.get(
            f"https://scratchdb.lefty.one/v3/user/graph/{self.username}/followers?segment={segment}&range={range}").text)

    def post_comment(self, content, commentee_id="", parent_id=""):
        """
        Post a comment on the user's profile
        :param content: The comment
        """
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

    def report(self, field):
        """
        Report a user
        :param field: The field or the reason of report.
        """
        if self.username != self.client_username:
            raise Exceptions.UnauthorizedAction("You are not allowed to do that")
        data = {"selected_field": field}
        requests.post(f"https://scratch.mit.edu/site-api/users/all/{self.username}/report/",
                      headers=self.headers,
                      data=json.dumps(data),
                      )

    def get_all_data(self):
        """
        Returns all the data of the user
        """
        data = {
            'UserName': self.username,
            'UserId': self.get_id(self.username),
            'Messages Count': self.get_messages_count(),
            'Join Date': self.get_joined_date(),
            'Status': self.get_status(),
            'Work': self.get_work(),
            'Bio': self.get_bio(),
            'Country': self.get_country(),
            'Follower Count': self.get_follower_count(),
            'Following Count': self.get_following_count(),
            'Total Views': self.get_total_views(),
            'Total Loves': self.get_total_loves(),
            'Total Favourites': self.get_total_favourites(),
            'Followers': self.get_followers(all=True),
            'Following': self.get_following(all=True),
            'Favourites': self.get_favourites(all=True),
            'Projects': self.get_projects(all=True)
        }
        return data

    def get_comments(self, limit=5, page=1):
        """
        Get comments of the profile of the user
        :param limit: The limit
        :param page: The page
        """
        return requests.get(f"https://scratch-profile-comments.sid72020123.repl.co/comments/?username={self.username}&limit={limit}&page={page}").json()

