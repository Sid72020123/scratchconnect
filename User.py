import requests
import json

import scratchconnect.Exceptions

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"https://api.{_website}"


class User:
    def __init__(self, username, client_username, csrf_token, session_id, token):
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
        try:
            json.loads(requests.get(f"{_api}/users/{username}").text)["id"]
        except KeyError:
            raise scratchconnect.Exceptions.InvalidUser(f"Username '{self.username}' doesn't exist!")

    def get_id(self, username):
        return json.loads(requests.get(f"{_api}/users/{username}").text)["id"]

    def get_messages_count(self):
        return json.loads(requests.get(f"https://api.scratch.mit.edu/users/{self.username}/messages/count").text)[
            "count"]

    def get_work(self):
        return json.loads(requests.get(self._user_link).text)["profile"]["status"]

    def get_bio(self):
        return json.loads(requests.get(self._user_link).text)["profile"]["bio"]

    def get_status(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["status"]

    def get_joined_date(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["joined"]

    def get_country(self):
        return json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{self.username}").text)["country"]

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

    def get_user_follower_history(self, segment="", range=30):
        return json.loads(requests.get(
            f"https://scratchdb.lefty.one/v3/user/graph/{self.username}/followers?segment={segment}&range={range}").text)

    def post_comment(self, content, commentee_id="", parent_id=""):
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
