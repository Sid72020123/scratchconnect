import requests
import json
import re

from scratchconnect import Exceptions
from scratchconnect import Project
from scratchconnect import User

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class ScratchConnect:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._login()

    def _login(self):
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
            json.loads(requests.get(f"https://{_api}/users/{username}").text)["id"]
        except KeyError:
            raise Exceptions.InvalidUser(f"Username '{username}' doesn't exist!")

    def get_id(self, username):
        return json.loads(requests.get(f"https://{_api}/users/{username}").text)["id"]

    def get_messages_count(self):
        return json.loads(requests.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count").text)[
            "count"]

    def get_messages(self, all=False, limit=20, offset=0):
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
                    f"https://api.scratch.mit.edu/users/{self.username}/messages/?limit=40&offset={offset}",
                    headers=headers).json()
                messages.append(request)
                if len(request) != 40:
                    break
                offset += 40
        if not all:
            messages = []
            for i in range(1, limit + 1):
                request = requests.get(
                    f"https://api.scratch.mit.edu/users/{self.username}/messages/?limit={limit}&offset={offset}",
                    headers=headers).json()
                messages.append(request)
        return messages

    def get_work(self):
        return json.loads(requests.get(_user_link).text)["profile"]["status"]

    def get_bio(self):
        return json.loads(requests.get(_user_link).text)["profile"]["bio"]

    def get_status(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["status"]

    def get_joined_date(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["joined"]

    def get_country(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["country"]

    def get_featured_data(self):
        return json.loads(requests.get(f"https://scratch.mit.edu/site-api/users/all/{self.username}").text)

    def get_projects(self, all=False, limit=20, offset=0):
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

    def get_follower_count(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "followers"]

    def get_following_count(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "following"]

    def get_total_views(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "views"]

    def get_total_loves(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "loves"]

    def get_total_favourites(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v2/user/info/{self.username}").text)["statistics"][
            "favorites"]

    def get_following(self, all=False, limit=40, offset=0):
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

    def toggle_commenting(self):
        return requests.post(
            "https://scratch.mit.edu/site-api/comments/user/"
            + self.username
            + "/toggle-comments/",
            headers=self.headers,
        )

    def follow_user(self, username):
        self.check(username)
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + username
            + "/add/?usernames="
            + self.username,
            headers=self.headers,
        )

    def unfollow_user(self, username):
        self.check(username)
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + username
            + "/remove/?usernames="
            + self.username,
            headers=self.headers,
        )

    def get_all_data(self):
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
        try:
            json.loads(requests.get(f"https://api.scratch.mit.edu/projects/{project_id}/").text)["id"]
        except KeyError:
            print("Error!")
    # Main
    def get_site_health(self):
        return json.loads(requests.get("https://api.scratch.mit.edu/health").text)

    def get_news(self):
        return json.loads(requests.get("https://api.scratch.mit.edu/news").text)

    def get_front_page_projects(self):
        return json.loads(requests.get("https://api.scratch.mit.edu/proxy/featured").text)

    def explore_projects(self, mode="trending", query="*"):
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/explore/projects/?mode="
            + mode
            + "&q="
            + query
        ).text)

    def explore_studios(self, mode="trending", query="*"):
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/explore/studios/?mode="
            + mode
            + "&q="
            + query
        ).text)

    def search_projects(self, mode="trending", search="*"):
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/search/projects/?mode="
            + mode
            + "&q="
            + search
        ).text)

    def search_studios(self, mode="trending", search="*"):
        return json.loads(requests.get(
            "https://api.scratch.mit.edu/search/studios/?mode="
            + mode
            + "&q="
            + search
        ).text)

    def set_featured_project(self, project_id, label='featured_project'):
        self._check_project(project_id)
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

    def connect_project(self, project_id):
        return Project.Project(project_id)

    def connect_user(self, username):
        return User.User(username=username, client_username=self.username, csrf_token=self.csrf_token,
                         session_id=self.session_id, token=self.token)
