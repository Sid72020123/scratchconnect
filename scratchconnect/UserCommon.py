"""
This File contains the functions used commonly by the ScratchConnect.py/ScratchConnect and User.py/User class
"""

import json
import requests

from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions

_website = "scratch.mit.edu"
_api = f"https://api.{_website}"


class UserCommon:
    def __init__(self, username, session, online_ide):
        """
        The User Class to connect a Scratch user.
        :param username: The username
        """
        self.username = username
        self.session = session
        self._user_link = f"{_api}/users/{self.username}"
        if online_ide:
            _change_request_url()
        self.update_data()

    def update_data(self) -> None:
        """
        Update the stored data
        """
        self.user_id = None
        self.user_messages_count = None
        self.user_messages = None
        self.user_work = None
        self.user_status = None
        self.user_joined_date = None
        self.user_country = None
        self.user_featured_data = None
        self.user_projects = None
        self.user_followers_count = None
        self.user_following_count = None
        self.user_total_views = None
        self.user_total_loves = None
        self.user_total_faves = None
        self.user_following = None
        self.user_followers = None
        self.user_favourites = None
        self.user_projects_count = None
        self.user_projects_count = None

        data = self.session.get(f"{self._user_link}").json()
        try:
            self.user_id = data["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{self.username}' doesn't exist!")
        self.user_work = data["profile"]["status"]
        self.user_bio = data["profile"]["bio"]
        self.user_joined_date = data["history"]["joined"]
        self.user_country = data["profile"]["country"]
        self.user_thumbnail_url = data["profile"]["images"]

    def _update_db_data(self):
        """
        Update the stored Data (DON'T USE)
        """
        try:
            data = requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").json()
            self.user_status = data["status"]
            self.user_followers_count = data["statistics"]["followers"]
            self.user_following_count = data["statistics"]["following"]
            self.user_total_views = data["statistics"]["views"]
            self.user_total_loves = data["statistics"]["loves"]
            self.user_total_faves = data["statistics"]["favorites"]
        except json.decoder.JSONDecodeError:
            pass

    def id(self) -> int:
        """
        Get the ID of a user's profile
        """
        if self.id is None:
            self.update_data()
        return self.user_id

    def thumbnail_url(self) -> dict:
        """Return the thumbnail URL of a user"""
        if self.user_thumbnail_url is None:
            self.update_data()
        return self.user_thumbnail_url

    def messages_count(self) -> int:
        """
        Get the messages count of the logged in user
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
        if self.user_messages_count is None:
            self.user_messages_count = \
                self.session.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count",
                                 headers=headers).json()[
                    "count"]
        return self.user_messages_count

    def work(self) -> str:
        """
        Returns the 'What I am working on' of a Scratch profile
        """
        if self.user_work is None:
            self.update_data()
        return self.user_work

    def bio(self) -> str:
        """
        Returns the 'About me' of a Scratch profile
        """
        if self.user_bio is None:
            self.update_data()
        return self.user_bio

    def status(self) -> str:
        """
        Returns the status(Scratcher or New Scratcher) of a Scratch profile
        """
        if self.user_status is None:
            self._update_db_data()
        return self.user_status

    def joined_date(self) -> str:
        """
        Returns the joined date of a Scratch profile
        """
        if self.user_joined_date is None:
            self.update_data()
        return self.user_joined_date

    def country(self) -> str:
        """
        Returns the country of a Scratch profile
        """
        if self.user_country is None:
            self.update_data()
        return self.user_country

    def followers_count(self) -> int:
        """
        Returns the follower count of a user
        """
        if self.user_followers_count is None:
            self._update_db_data()
        return self.user_followers_count

    def following_count(self) -> int:
        """
        Returns the following count of a user
        """
        if self.user_following_count is None:
            self._update_db_data()
        return self.user_following_count

    def total_views(self) -> int:
        """
        Returns the total views count of all the shared projects of a user
        """
        if self.user_total_views is None:
            self._update_db_data()
        return self.user_total_views

    def total_loves_count(self) -> int:
        """
        Returns the total loves count of all the shared projects of a user
        """
        if self.user_total_loves is None:
            self._update_db_data()
        return self.user_total_loves

    def total_favourites_count(self) -> int:
        """
        Returns the total favourites count of all the shared projects of a user
        """
        if self.user_total_faves is None:
            self._update_db_data()
        return self.user_total_faves

    def featured_data(self) -> dict:
        """
        Returns the featured project data of the Scratch profile
        """
        if self.user_featured_data is None:
            self.user_featured_data = self.session.get(
                f"https://scratch.mit.edu/site-api/users/all/{self.username}").json()
        return self.user_featured_data

    def projects(self, all=False, limit=20, offset=0) -> list:
        """
        Returns the list of shared projects of a user
        :param all: If you want all then set it to True
        :param limit: The limit of the projects
        :param offset: The number of projects to be skipped from the beginning
        """
        if self.user_projects is None:
            projects = []
            if all:
                offset = 0
                while True:
                    request = self.session.get(
                        f"{_api}/users/{self.username}/projects/?limit=40&offset={offset}").json()
                    projects.append(request)
                    if len(request) != 40:
                        break
                    offset += 40
            if not all:
                for i in range(1, limit + 1):
                    request = self.session.get(
                        f"{_api}/users/{self.username}/projects/?limit={limit}&offset={offset}").json()
                    projects.append(request)
            self.user_projects = projects
        return self.user_projects

    def projects_count(self) -> int:
        if self.user_projects_count is None:
            all_projects = self.projects(all=True)
            count = 0
            for i in all_projects:
                count += len(i)
            self.user_projects_count = count
        return self.user_projects_count

    def following(self, all=False, limit=20, offset=0) -> list:
        """
        Returns the list of the user following
        :param all: If you want all then set it to True
        :param limit: The limit of the users
        :param offset: The number of users to be skipped from the beginning
        """
        if self.user_following is None:
            following = []
            if all:
                offset = 0
                while True:
                    response = self.session.get(
                        f"{_api}/users/{self.username}/following/?limit=40&offset={offset}").json()
                    offset += 40
                    following.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = self.session.get(
                    f"{_api}/users/{self.username}/following/?limit={limit}&offset={offset}").json()
                following.append(response)
            self.user_following = following
        return self.user_following

    def followers(self, all=False, limit=20, offset=0) -> list:
        """
        Returns the list of the user followers
        :param all: If you want all then set it to True
        :param limit: The limit of the users
        :param offset: The number of users to be skipped from the beginning
        """
        if self.user_followers is None:
            followers = []
            if all:
                offset = 0
                while True:
                    response = self.session.get(
                        f"{_api}/users/{self.username}/followers/?limit=40&offset={offset}").json()
                    offset += 40
                    followers.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = self.session.get(
                    f"{_api}/users/{self.username}/followers/?limit={limit}&offset={offset}").json()
                followers.append(response)
            self.user_followers = followers
        return self.user_followers

    def favourites(self, all=False, limit=20, offset=0) -> list:
        """
        Returns the list of the user favourites
        :param all: If you want all then set it to True
        :param limit: The limit of the projects
        :param offset: The number of projects to be skipped from the beginning
        """
        if self.user_favourites is None:
            favourites = []
            if all:
                offset = 0
                while True:
                    response = self.session.get(
                        f"{_api}/users/{self.username}/favorites/?limit=40&offset={offset}").json()
                    offset += 40
                    favourites.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = self.session.get(
                    f"{_api}/users/{self.username}/favorites/?limit={limit}&offset={offset}").json()
                favourites.append(response)
            self.user_favourites = favourites
        return self.user_favourites

    def user_follower_history(self, segment="", range=30) -> list:
        """
        Return the follower history of the user
        :param segment: The length of time between each segment, defaults to 1 day.
        :param range: Of how far back to get history, defaults to 30 days
        """
        return requests.get(
            f"https://scratchdb.lefty.one/v3/user/graph/{self.username}/followers?segment={segment}&range={range}").json()

    def all_data(self) -> dict:
        """
        Returns all the data of the user
        """
        data = {
            'UserName': self.username,
            'UserId': self.id(),
            'Messages Count': self.messages_count(),
            'Join Date': self.joined_date(),
            'Status': self.status(),
            'Work': self.work(),
            'Bio': self.bio(),
            'Country': self.country(),
            'Follower Count': self.followers_count(),
            'Following Count': self.following_count(),
            'Total Views': self.total_views(),
            'Total Loves': self.total_loves_count(),
            'Total Favourites': self.total_favourites_count(),
            'Total Projects Count': self.projects_count()
        }
        return data

    def ocular_data(self) -> dict:
        """
        Get ocular data of the user
        """
        return requests.get(f"https://my-ocular.jeffalo.net/api/user/{self.username}").json()

    def aviate_data(self, code=False) -> dict:
        """
        Get Aviate Status of the user
        :param code: True to get the status code
        """
        return requests.get(f"https://aviateapp.eu.org/api/{self.username}?code={str(code).lower()}").json()['status']

    def comments(self, limit=5, page=1) -> dict:
        """
        Get comments of the profile of the user
        :param limit: The limit
        :param page: The page
        """
        return requests.get(
            f"https://apis.scratchconnect.eu.org/comments/user/?username={self.username}&limit={limit}&page={page}").json()
