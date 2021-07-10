import json
import requests
import websocket
import time

from scratchconnect import Exceptions

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
        self._make_connection()

    def get_variable_data(self, limit=100, offset=0):
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

    def get_cloud_variable_value(self, variable_name, limit=100):
        if str(variable_name.strip())[0] != "☁":
            n = f"☁ {variable_name.strip()}"
        else:
            n = f"{variable_name.strip()}"
        data = []
        d = self.get_variable_data(limit=limit)
        i = 0
        while i < len(d):
            if d[i]['Name'] == n:
                data.append(d[i]['Value'])
            i = i + 1
        return data

    def _send_packet(self, packet):
        self._ws.send(json.dumps(packet) + "\n")

    def _make_connection(self):
        self._ws = websocket.WebSocket()
        self._ws.connect(
            "wss://clouddata.scratch.mit.edu",
            cookie=f"scratchsessionsid={self.session_id};",
            origin="https://scratch.mit.edu",
            enable_multithread=True,
            subprotocols=["binary", "base64"]
        )
        self._send_packet(
            {
                "method": "handshake",
                "user": self.client_username,
                "project_id": str(self.project_id),
            }
        )

    def set_cloud_variable(self, variable_name, value):
        if not str(value).isdigit():
            raise Exceptions.InvalidCloudValue(f"The Cloud Value should be a set of digits and not '{value}'!")
        try:
            if str(variable_name.strip())[0] != "☁":
                n = f"☁ {variable_name.strip()}"
            else:
                n = f"{variable_name.strip()}"
            packet = {
                "method": "set",
                "name": n,
                "value": str(value),
                "user": self.client_username,
                "project_id": str(self.project_id),
            }
            self._send_packet(packet)
            return True
        except ConnectionAbortedError or BrokenPipeError:
            self._make_connection()
            time.sleep(0.1)
            self.set_cloud_variable(variable_name, value)
            return False
