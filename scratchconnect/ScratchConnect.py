"""
Main File to Connect all the Scratch API and the Scratch DB
"""

import requests
import json
import re

from scratchconnect.UserCommon import UserCommon
from scratchconnect import Exceptions
from scratchconnect import Warnings
from scratchconnect import Project
from scratchconnect import Studio
from scratchconnect import User
from scratchconnect import Forum
from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect.scScratchTerminal import _terminal
from scratchconnect.scChart import _chart
from scratchconnect.scImage import Image

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class ScratchConnect(UserCommon):
    def __init__(self, username=None, password=None, cookie=None, auto_cookie_login=False, online_ide_cookie=None):
        """
        Class to make a connection to Scratch
        :param username: The username of a Scratch Profile
        :param password: The password of a Scratch Profile
        """
        self.username = username
        self.password = password
        self.cookie = cookie
        self.session = None
        self._online_ide = False
        self.auto_cookie_login = auto_cookie_login
        self.online_ide_cookie = online_ide_cookie

        if self.username is not None and self.password is not None:
            self._login(cookie=False, auto_cookie_login=self.auto_cookie_login)
            self._logged_in = True
        elif self.cookie is not None:
            self._login(cookie=True, auto_cookie_login=self.auto_cookie_login)
            self._logged_in = True
        elif self.online_ide_cookie is not None:
            _change_request_url()
            self._online_ide = True
            self._login(online_ide=True)
            self._logged_in = True
        else:
            self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self._logged_in = False
            self.session_id = ""
            self.headers = {
                "x-csrftoken": "",
                "X-Token": "",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken="
                          + ""
                          + ";scratchlanguage=en;scratchsessionsid="
                          + ""
                          + ";",
                "referer": "https://scratch.mit.edu",
            }
            Warnings.warn(
                "[1m[33mScratchConnect: [31mLogin with Username/Password and Cookie Failed! Continuing without login...[0m")
        super().__init__(self.username,
                         self.headers,
                         self._online_ide)  # Get other properties and methods from the parent(UserCommon) class
        self.update_data()

    def _login(self, cookie=False, auto_cookie_login=False, online_ide=False):
        """
        Function to login(don't use this)
        """
        global _user_link
        if cookie is False and online_ide is False:
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
                request.json()
            except Exception:
                if request.status_code == 403:  # *
                    if auto_cookie_login is True:
                        self._cookie_login()
                    else:
                        Warnings.warn(
                            """[33m[1mScratchConnect: [31mScratch is not letting you login from this device.\n[35mTry to do the following to fix this issue:\n[36m- Try again later (10-15 minutes)\n[36m- Use Cookie login - [4mhttps://github.com/Sid72020123/scratchconnect#Cookie-Login[0m\n[36m[1m- Try from another device (Scratch sometimes blocks login from Replit)[0m""")
            try:
                self.session_id = re.search('"(.*)"', request.headers["Set-Cookie"]).group()
                self._get_token()
            except AttributeError:
                if auto_cookie_login is True:
                    self._cookie_login()
                else:
                    raise Exceptions.InvalidInfo('Invalid Username or Password!')
            self._get_csrf_token()
            _user_link = f"https://{_api}/users/{self.username}/"
        elif cookie is not False:
            self._cookie_login()
        elif online_ide is not False:
            self._online_ide_login()

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

    def _get_csrf_token(self):
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
            "referer": "https://scratch.mit.edu",
        }
        request = requests.get("https://scratch.mit.edu/csrf_token/", headers=headers)
        self.csrf_token = re.search("scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]).group(1)

    def _get_token(self):
        response = requests.post("https://scratch.mit.edu/session", headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://scratch.mit.edu",
        }, cookies={"scratchsessionsid": self.session_id, "scratchcsrftoken": "a", "scratchlanguage": "en"}).json()
        self.token = response['user']['token']
        self.session = response
        if self.session["user"]["banned"]:
            raise Exceptions.UnauthorizedAction(
                "You are banned on Scratch! You cannot login from ScratchConnect unless you are unbanned! This error is raised because ScratchConnect won't allow the banned users to login and do something inappropriate!")

    def _cookie_login(self):
        if self.cookie is None:
            raise Exceptions.InvalidInfo("Cookie Not Provided!")
        try:
            self.username = self.cookie["Username"]
            self.session_id = self.cookie["SessionID"]
        except KeyError:
            raise Exceptions.InvalidInfo("Required Cookie Headers are missing!")
        try:
            self._get_token()
            self._get_csrf_token()
            Warnings.warn(
                "[1m[33mScratchConnect: [31mYou are logging in with cookie. Some features might not work if the cookie values are wrong![0m")
        except KeyError:
            Warnings.warn(
                "[1m[33mScratchConnect: [31mCookie Login Failed because the cookie values may be wrong![0m")
            self.csrf_token = ""
            self.token = ""

    def _online_ide_login(self):
        if self.online_ide_cookie is None:
            raise Exceptions.InvalidInfo("Cookie Info Not Provided!")
        try:
            self.username = self.online_ide_cookie["Username"]
            self.session_id = self.online_ide_cookie["SessionID"]
        except KeyError:
            raise Exceptions.InvalidInfo("Required Cookie Headers are missing!")
        try:
            self._get_token()
            self._get_csrf_token()
            Warnings.warn(
                "[1m[33mScratchConnect: [31mYou are logging in on Replit or some other online IDE. Some features might not work if the cookie values are wrong or it may be slow! Also, you can't do any social interactions![0m")
        except (KeyError, TypeError, ValueError):
            Warnings.warn(
                "[1m[33mScratchConnect: [31mFetching token or csrf_token failed! You can still continue but social interactions won't work![0m")
            self.csrf_token = ""
            self.token = ""

    def check(self, username):
        try:
            requests.get(f"https://{_api}/users/{username}").json()["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def messages(self, all=False, limit=20, offset=0, filter="all"):
        """
        Get the list of messages
        :param all: True if you want all the messages
        :param limit: The limit of the messages
        :param offset: The number of messages to be skipped from the beginning
        :param filter: Filter the messages
        :return: The list of the messages
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
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

    def clear_messages(self):
        """
        Clear the messages
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return requests.post(f"https://scratch.mit.edu/site-api/messages/messages-clear/", headers=self.headers).text

    def my_stuff_projects(self, order="all", page=1, sort_by=""):
        """
        Get the projects in the MyStuff section of the logged in user
        :param order: the order
        :param page: the page
        :param sort_by: sort
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return requests.get(
            f"https://scratch.mit.edu/site-api/projects/{order}/?page={page}&ascsort=&descsort={sort_by}",
            headers=self.headers).json()

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

    def _check_project(self, project_id):
        """
        Don't use this function
        """
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            raise Exceptions.InvalidProject(f"The project with ID - '{project_id}' doesn't exist!")

    def feed(self, limit=40, offset=0):
        """
        Returns the "What's Happening" section of the front page
        :param limit: the limit; max: 40
        :param offset: the offset
        """
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
        return requests.get(
            f"https://api.scratch.mit.edu/users/{self.username}/following/users/activity?limit={limit}&offset={offset}",
            headers=self.headers).json()

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
        if self._logged_in is False:
            raise Exceptions.UnauthorizedAction("Cannot perform the action because the user is not logged in!")
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

    def search_forum(self, q, order="relevance", page=0):
        """
        Search the forum
        :param q: query
        :param order: The order. Use values like "relevance", "newest", "oldest"
        :param page: page
        """
        return requests.get(f"https://scratchdb.lefty.one/v3/forum/search?q={q}&o={order}&page={page}").json()

    def connect_user(self, username):
        """
        Connect a Scratch User
        :param username: A valid Username
        """
        return User.User(username=username, client_username=self.username, headers=self.headers,
                         logged_in=self._logged_in, online_ide=self._online_ide)

    def connect_studio(self, studio_id):
        """
        Connect a Scratch Studio
        :param studio_id: A valid studio ID
        """
        return Studio.Studio(id=studio_id, client_username=self.username, headers=self.headers,
                             logged_in=self._logged_in, online_ide=self._online_ide)

    def connect_project(self, project_id, access_unshared=False):
        """
        Connect a Scratch Project
        :param project_id: A valid project ID
        :param access_unshared: Set to True if you want to connect an unshared project
        """
        return Project.Project(id=project_id, client_username=self.username, headers=self.headers,
                               logged_in=self._logged_in, unshared=access_unshared, session_id=self.session_id,
                               online_ide=self._online_ide)

    def connect_forum_topic(self, forum_id):
        """
        Connect a Scratch Forum Topic
        :param forum_id: A valid forum topic ID
        """
        return Forum.Forum(id=forum_id, client_username=self.username, headers=self.headers, logged_in=self._logged_in,
                           online_ide=self._online_ide)

    def create_new_terminal(self):
        """
        Create a new Terminal object
        """
        return _terminal(sc=self)

    def create_new_chart(self):
        """
        Create a new Chart object
        """
        return _chart(sc=self)

    def create_new_image(self):
        """
        Create a new scImage object
        """
        return Image(online_ide=self._online_ide)
