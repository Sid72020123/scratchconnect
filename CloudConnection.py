import json
import requests
import websocket

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class CloudConnection:
    def __init__(self, project_id, client_username, csrf_token, session_id, token):
        self.project_id = str(project_id)
        self.client_username = client_username
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
            "referer": "https://scratch.mit.edu/projects/" + self.project_id + "/",
        }

        self.json_headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self.session_id
                      + ";",
            "referer": "https://scratch.mit.edu/projects/" + str(self.project_id) + "/",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_variable_data(self, limit=1000, offset=0):
        response = requests.get(
            f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit={limit}&offset={offset}").json()
        data = []
        for i in range(0, len(response)):
            data.append({'User': response[i]['user'],
                         'Action': response[i]['verb'],
                         'Name': response[i]['name'],
                         'Value': response[i]['value'],
                         })
        return data
