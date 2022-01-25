"""
Main File to Connect all the Scratch API and the Scratch DB
"""
import requests
import json
import re

from scratchconnect import Exceptions
from scratchconnect import Project
from scratchconnect import Studio
from scratchconnect import User
from scratchconnect import Forum

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class ScratchConnect:
    def __init__(self, username, password):
        """
        Class to make a connection to Scratch
        :param username: The username of a Scratch Profile
        :param password: The password of a Scratch Profile
        """
        self.username = username
        self.password = password

        self._login()
        self.update_data()

    def _login(self):
        """
        Function to login(don't use this)
        """
        global _user_link
        headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
        }
        data = json.dumps({"username": self.username, "password": self.password})
        request = requests.post(f"{_login}", data=data, headers=headers)
        try:
            self.session_id = re.search('"(.*)"', request.headers["Set-Cookie"]).group()
            self.token = request.json()[0]["token"]
        except AttributeError:
            raise Exceptions.InvalidInfo('Invalid Username or Password!')
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
            "referer": "https://scratch.mit.edu",
        }
        request = requests.get("https://scratch.mit.edu/csrf_token/", headers=headers)
        self.csrf_token = re.search("scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]).group(1)
        _user_link = f"https://{_api}/users/{self.username}/"
        self.headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self.session_id
                      + ";",
            "referer": "https://scratch.mit.edu",
        }

    def check(self, username):
        try:
            requests.get(f"https://{_api}/users/{username}").json()["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def update_data(self):
        """
        Update the stored data
        """
        self.user_id = None
        self.user_thumbnail_url = None
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

        data = requests.get(f"https://{_api}/users/{self.username}").json()
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
        data = requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").json()
        self.user_status = data["status"]
        self.user_followers_count = data["statistics"]["followers"]
        self.user_following_count = data["statistics"]["following"]
        self.user_total_views = data["statistics"]["views"]
        self.user_total_loves = data["statistics"]["loves"]
        self.user_total_faves = data["statistics"]["favorites"]

    def id(self):
        """
        Get the ID of a user's profile
        """
        if self.id is None:
            self.update_data()
        return self.user_id

    def thumbnail_url(self):
        """Return the thumbnail URL of a user"""
        if self.user_thumbnail_url is None:
            self.update_data()
        return self.user_thumbnail_url

    def messages_count(self):
        """
        Get the messages count of the logged in user
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
        if self.user_messages_count is None:
            self.user_messages_count = \
                requests.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count",
                             headers=headers).json()[
                    "count"]
        return self.user_messages_count

    def messages(self, all=False, limit=20, offset=0, filter="all"):
        """
        Get the list of messages
        :param all: True if you want all the messages
        :param limit: The limit of the messages
        :param offset: The number of messages to be skipped from the beginning
        :param filter: Filter the messages
        :return: The list of the messages
        """
        headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self.session_id
                      + ";",
            "referer": "https://scratch.mit.edu",
        }
        if self.user_messages is None:
            messages = []
            if all:
                offset = 0
                while True:
                    request = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/messages/?limit=40&offset={offset}&filter={filter}",
                        headers=headers).json()
                    messages.append(request)
                    if len(request) != 40:
                        break
                    offset += 40
            if not all:
                for i in range(1, limit + 1):
                    request = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/messages/?limit={limit}&offset={offset}&filter={filter}",
                        headers=headers).json()
                    messages.append(request)
            self.user_messages = messages
        return self.user_messages

    def work(self):
        """
        Returns the 'What I am working on' of a Scratch profile
        """
        if self.user_work is None:
            self.update_data()
        return self.user_work

    def bio(self):
        """
        Returns the 'About me' of a Scratch profile
        """
        if self.user_bio is None:
            self.update_data()
        return self.user_bio

    def status(self):
        """
        Returns the status(Scratcher or New Scratcher) of a Scratch profile
        """
        if self.user_status is None:
            self._update_db_data()
        return self.user_status

    def joined_date(self):
        """
        Returns the joined date of a Scratch profile
        """
        if self.user_joined_date is None:
            self.update_data()
        return self.user_joined_date

    def country(self):
        """
        Returns the country of a Scratch profile
        """
        if self.user_country is None:
            self.update_data()
        return self.user_country

    def featured_data(self):
        """
        Returns the featured project data of the Scratch profile
        """
        if self.user_featured_data is None:
            self.user_featured_data = requests.get(f"https://scratch.mit.edu/site-api/users/all/{self.username}").json()
        return self.user_featured_data

    def projects(self, all=False, limit=20, offset=0):
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
                    request = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit=40&offset={offset}").json()
                    projects.append(request)
                    if len(request) != 40:
                        break
                    offset += 40
            if not all:
                for i in range(1, limit + 1):
                    request = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit={limit}&offset={offset}").json()
                    projects.append(request)
            self.user_projects = projects
        return self.user_projects

    def projects_count(self):
        if self.user_projects_count is None:
            all_projects = self.projects(all=True)
            count = 0
            for i in all_projects:
                count += len(i)
            self.user_projects_count = count
        return self.user_projects_count

    def followers_count(self):
        """
        Returns the follower count of a user
        """
        if self.user_followers_count is None:
            self._update_db_data()
        return self.user_followers_count

    def following_count(self):
        """
        Returns the following count of a user
        """
        if self.user_following_count is None:
            self._update_db_data()
        return self.user_following_count

    def total_views(self):
        """
        Returns the total views count of all the shared projects of a user
        """
        if self.user_total_views is None:
            self._update_db_data()
        return self.user_total_views

    def total_loves_count(self):
        """
        Returns the total loves count of all the shared projects of a user
        """
        if self.user_total_loves is None:
            self._update_db_data()
        return self.user_total_loves

    def total_favourites_count(self):
        """
        Returns the total favourites count of all the shared projects of a user
        """
        if self.user_total_faves is None:
            self._update_db_data()
        return self.user_total_faves

    def following(self, all=False, limit=20, offset=0):
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
                    response = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/following/?limit=40&offset={offset}").json()
                    offset += 40
                    following.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/following/?limit={limit}&offset={offset}").json()
                following.append(response)
            self.user_following = following
        return self.user_following

    def followers(self, all=False, limit=20, offset=0):
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
                    response = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit=40&offset={offset}").json()
                    offset += 40
                    followers.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit={limit}&offset={offset}").json()
                followers.append(response)
            self.user_followers = followers
        return self.user_followers

    def favourites(self, all=False, limit=20, offset=0):
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
                    response = requests.get(
                        f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit=40&offset={offset}").json()
                    offset += 40
                    favourites.append(response)
                    if len(response) != 40:
                        break
            if not all:
                response = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit={limit}&offset={offset}").json()
                favourites.append(response)
            self.user_favourites = favourites
        return self.user_favourites

    def toggle_commenting(self):
        """
        Toggle the commenting of the profile
        """
        return requests.post(
            "https://scratch.mit.edu/site-api/comments/user/"
            + self.username
            + "/toggle-comments/",
            headers=self.headers,
        )

    def follow_user(self, username):
        """
        Follow a user
        :param username: The username
        """
        self.check(username)
        if username == self.username:
            raise Exceptions.UnauthorizedAction(f"You can't follow yourself!")
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + username
            + "/add/?usernames="
            + self.username,
            headers=self.headers,
        )

    def unfollow_user(self, username):
        """
        UnFollow a user
        :param username: The username
        """
        self.check(username)
        if username == self.username:
            raise Exceptions.UnauthorizedAction(f"You can't unfollow yourself!")
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + username
            + "/remove/?usernames="
            + self.username,
            headers=self.headers,
        )

    def set_bio(self, content):
        """
        Set the bio or 'About Me' of the profile
        :param content: The bio or the content.
        Thanks to QuantumCodes for helping me in the error!
        """
        data = json.dumps({"bio": content})
        return requests.put(f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
                            data=data,
                            headers=self.headers,
                            )

    def set_work(self, content):
        """
        Set the status or 'What I am Working On' of the profile
        :param content: The work or the content.
        Thanks to QuantumCodes for helping me in the error!
        """
        data = json.dumps({"status": content})
        return requests.put(f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
                            data=data,
                            headers=self.headers,
                            )

    def all_data(self):
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

    def _check_project(self, project_id):
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def site_health(self):
        """
        Returns the health of the Scratch Website.
        """
        return requests.get("https://api.scratch.mit.edu/health").json()

    def site_news(self):
        """
        Returns the news of the Scratch Website.
        """
        return requests.get("https://api.scratch.mit.edu/news").json()

    def site_front_page_projects(self):
        """
        Returns the front page projects of the Scratch Website.
        """
        return requests.get("https://api.scratch.mit.edu/proxy/featured").json()

    def explore_projects(self, mode="trending", query="*"):
        """
        Explore the projects
        :param mode: The mode such as 'popular' or 'trending'
        :param query: The query
        """
        return requests.get(
            "https://api.scratch.mit.edu/explore/projects/?mode="
            + mode
            + "&q="
            + query
        ).json()

    def explore_studios(self, mode="trending", query="*"):
        """
        Explore the studios
        :param mode: The mode such as 'popular' or 'trending'
        :param query: The query
        """
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/explore/studios/?mode="
            + mode
            + "&q="
            + query
        ).text)

    def search_projects(self, mode="trending", search="*"):
        """
        Search the projects
        :param mode: The mode such as 'popular' or 'trending'
        :param query: The query
        """
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/search/projects/?mode="
            + mode
            + "&q="
            + search
        ).text)

    def search_studios(self, mode="trending", search="*"):
        """
        Search the studios
        :param mode: The mode such as 'popular' or 'trending'
        :param query: The query
        """
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/search/studios/?mode="
            + mode
            + "&q="
            + search
        ).text)

    def comments(self, limit=5, page=1):
        """
        Get comments of the profile of the user
        :param limit: The limit
        :param page: The page
        """
        return requests.get(
            f"https://scratch-comments-api.sid72020123.repl.co/user/?username={self.username}&limit={limit}&page={page}").json()

    def set_featured_project(self, project_id, label='featured_project'):
        """
        Set the 'Featured Project' of a Scratch Profile
        :param project_id: The project id
        :param label: The Label, options:
                "featured_project": "",
                "featured_tutorial": 0,
                "work_in_progress": 1,
                "remix_this": 2,
                "my_favorite_things": 3,
                "why_i_scratch": 4,
        """
        self._check_project(project_id)
        if not requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").json()["author"][
                   "username"] == self.username:
            raise Exceptions.UnauthorizedAction(
                f"The project with ID - '{project_id}' cannot be set because the owner of that project is not '{self.username}'!")
        _label = (
            {
                "featured_project": "",
                "featured_tutorial": 0,
                "work_in_progress": 1,
                "remix_this": 2,
                "my_favorite_things": 3,
                "why_i_scratch": 4,
            }
        )[label]
        data = {"featured_project": project_id, "featured_project_label": _label}
        return requests.put(f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
                            data=json.dumps(data),
                            headers=self.headers,
                            ).json()

    def user_follower_history(self, segment="", range=30):
        """
        Return the follower history of the user
        :param segment: The length of time between each segment, defaults to 1 day.
        :param range: Of how far back to get history, defaults to 30 days
        """
        return requests.get(
            f"https://scratchdb.lefty.one/v3/user/graph/{self.username}/followers?segment={segment}&range={range}").json()

    def connect_user(self, username):
        """
        Connect a Scratch User
        :param username: A valid Username
        """
        return User.User(username=username, client_username=self.username, csrf_token=self.csrf_token,
                         session_id=self.session_id, token=self.token)

    def connect_studio(self, studio_id):
        """
        Connect a Scratch Studio
        :param studio_id: A valid studio ID
        """
        return Studio.Studio(id=studio_id, client_username=self.username, csrf_token=self.csrf_token,
                             session_id=self.session_id, token=self.token)

    def connect_project(self, project_id, access_unshared=False):
        """
        Connect a Scratch Project
        :param project_id: A valid project ID
        """
        return Project.Project(id=project_id, client_username=self.username, csrf_token=self.csrf_token,
                               session_id=self.session_id, token=self.token, unshared=access_unshared)

    def connect_forum_topic(self, forum_id):
        """
        Connect a Scratch Forum Topic
        :param forum_id: A valid forum topic ID
        """
        return Forum.Forum(id=forum_id, client_username=self.username, csrf_token=self.csrf_token,
                           session_id=self.session_id, token=self.token)
