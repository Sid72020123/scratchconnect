"""
Main File to Connect all the Scratch API nad Scratch DB
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
        """
        Check if a username exists
        :param username: The username
        """
        try:
            json.loads(requests.get(f"https://{_api}/users/{username}").text)["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def get_id(self, username=None):
        """
        Get the ID of a user's profile
        :param username: The username
        """
        if username is None:
            username = self.username
        return json.loads(requests.get(f"https://{_api}/users/{username}").text)["id"]

    def get_messages_count(self):
        """
        Get the messages count of the logged in user
        """
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
        return json.loads(requests.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count", headers=headers).text)[
            "count"]

    def get_messages(self, all=False, limit=20, offset=0, filter="all"):
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
        if all:
            messages = []
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
            messages = []
            for i in range(1, limit + 1):
                request = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/messages/?limit={limit}&offset={offset}&filter={filter}",
                    headers=headers).json()
                messages.append(request)
        return messages

    def get_work(self):
        """
        Returns the 'What I am working on' of a Scratch profile
        """
        return json.loads(requests.get(_user_link).text)["profile"]["status"]

    def get_bio(self):
        """
        Returns the 'About me' of a Scratch profile
        """
        return json.loads(requests.get(_user_link).text)["profile"]["bio"]

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
                    f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit=40&offset={offset}").json()
                projects.append(request)
                if len(request) != 40:
                    break
                offset += 40
        if not all:
            projects = []
            for i in range(1, limit + 1):
                request = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/projects/?limit={limit}&offset={offset}").json()
                projects.append(request)
        return projects

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
                    f"https://api.scratch.mit.edu/users/{self.username}/following/?limit=40&offset={offset}").json()
                offset += 40
                following.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/following/?limit={limit}&offset={offset}").json()
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
                    f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit=40&offset={offset}").json()
                offset += 40
                followers.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/followers/?limit={limit}&offset={offset}").json()
            print(response)
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
                    f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit=40&offset={offset}").json()
                offset += 40
                favorites.append(response)
                if len(response) != 40:
                    break
        if not all:
            response = requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/favorites/?limit={limit}&offset={offset}").json()
            favorites.append(response)
        return favorites

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
        """
        data = {"bio": content}
        return requests.put(f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
                            data=data,
                            headers=self.headers,
                            )

    def set_work(self, content):
        """
        Set the status or 'What I am Working On' of the profile
        :param content: The work or the content.
        """
        data = {"status": content}
        return requests.put(f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
                            data=data,
                            headers=self.headers,
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

    def _check_project(self, project_id):
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def get_site_health(self):
        """
        Returns the health of the Scratch Website.
        """
        return json.loads(requests.get("https://api.scratch.mit.edu/health").text)

    def get_news(self):
        """
        Returns the news of the Scratch Website.
        """
        return json.loads(requests.get("https://api.scratch.mit.edu/news").text)

    def get_front_page_projects(self):
        """
        Returns the front page projects of the Scratch Website.
        """
        return json.loads(requests.get("https://api.scratch.mit.edu/proxy/featured").text)

    def explore_projects(self, mode="trending", query="*"):
        """
        Explore the projects
        :param mode: The mode such as 'popular' or 'trending'
        :param query: The query
        """
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/explore/projects/?mode="
            + mode
            + "&q="
            + query
        ).text)

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

    def get_comments(self, limit=5, page=1):
        """
        Get comments of the profile of the user
        :param limit: The limit
        :param page: The page
        """
        return requests.get(f"https://scratch-profile-comments.sid72020123.repl.co/comments/?username={self.username}&limit={limit}&page={page}").json()

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
        if not json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["author"][
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
        return json.loads(requests.put(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/",
            data=json.dumps(data),
            headers=self.headers,
        ).text)

    def get_user_follower_history(self, segment="", range=30):
        """
        Return the follower history of the user
        :param segment: The length of time between each segment, defaults to 1 day.
        :param range: Of how far back to get history, defaults to 30 days
        """
        return json.loads(requests.get(
            f"https://scratchdb.lefty.one/v3/user/graph/{self.username}/followers?segment={segment}&range={range}").text)

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

    def connect_project(self, project_id):
        """
        Connect a Scratch Project
        :param project_id: A valid project ID
        """
        return Project.Project(id=project_id, client_username=self.username, csrf_token=self.csrf_token,
                               session_id=self.session_id, token=self.token)

    def connect_forum_topic(self, forum_id):
        """
        Connect a Scratch Forum Topic
        :param forum_id: A valid forum topic ID
        """
        return Forum.Forum(id=forum_id, client_username=self.username, csrf_token=self.csrf_token,
                           session_id=self.session_id, token=self.token)
