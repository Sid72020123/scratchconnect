"""
The Cloud Variables File.
Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Encode/Decode Engine!
"""
import json
import requests  # Needed to change the URL of the request while using the online IDE
from ssl import SSLEOFError, SSLError
import websocket
import time
from threading import Thread

from scratchconnect.scOnlineIDE import _change_request_url
from scratchconnect import Exceptions
from scratchconnect.scEncoder import Encoder
from scratchconnect.scCloudEvents import CloudEvents

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class CloudConnection:
    def __init__(self, project_id, client_username, csrf_token, session_id, token, session, online_ide):
        """
        Main class to connect cloud variables
        """
        self.project_id = str(project_id)
        self.client_username = client_username
        self.csrf_token = csrf_token
        self.session_id = session_id
        self.token = token
        self.session = session
        self.headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};",
            "referer": "https://scratch.mit.edu/projects/" + self.project_id + "/",
        }

        self.json_headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};",
            "referer": "https://scratch.mit.edu/projects/" + str(self.project_id) + "/",
            "accept": "application/json",
            "Content-Type": "application/json",
            "origin": f"https://{_website}"
        }
        if online_ide:
            _change_request_url()
        self._event = CloudEvents("Scratch", self)
        self.encoder = Encoder()
        self._make_connection()
        self._start_ping_thread()

    def get_variable_data(self, limit: int = 100, offset: int = 0) -> list:
        """
        Returns the cloud variable data
        :param limit: The limit
        :param offset: The offset or the number of values you want to skip from the beginning
        """
        response = self.session.get(
            f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit={limit}&offset={offset}").json()
        data = []
        for i in range(0, len(response)):
            data.append({'User': response[i]['user'],
                         'Action': response[i]['verb'],
                         'Name': response[i]['name'],
                         'Value': response[i]['value'],
                         'Timestamp': response[i]['timestamp']
                         })
        return data

    def get_cloud_variable_value(self, variable_name: str, limit: int = 100) -> list:
        """
        Returns the cloud variable value as a list. The first of the list is the latest value
        :param variable_name: The name of the variable
        :param limit: The limit
        """
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
        """
        Don't use this
        """
        self._ws.send(json.dumps(packet) + "\n")

    def _ping_task(self):
        """
        Don't use this
        """
        while True:
            self._ws.ping()
            time.sleep(1)
            self._ws.pong()
            time.sleep(4)

    def _start_ping_thread(self):
        """
        Don't use this
        """
        self.ping_task = Thread(target=self._ping_task, daemon=True)
        self.ping_task.start()

    def _make_connection(self):
        """
        Don't use this
        """
        self._ws = websocket.WebSocket(enable_multithread=True)
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
        self._event.emit('connect')

    def set_cloud_variable(self, variable_name: str, value: int | str) -> bool:
        """
        Set a cloud variable
        :param variable_name: Variable name
        :param value: Variable value
        """
        if str(value).isdigit() and value == '':
            raise Exceptions.InvalidCloudValue(f"The Cloud Value should be a set of digits and not '{value}'!")

        try:
            if len(str(value)) > 256:
                raise ValueError(
                    "Scratch has Cloud Variable Limit of 256 Characters per variable. Try making the value shorter!")
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
        except (ConnectionAbortedError, BrokenPipeError, SSLEOFError, SSLError):
            self._event.emit('disconnect')
            self._make_connection()
            return False

    def encode(self, text: str, default: str = " ") -> str:
        """
        Encode a text. For example: A -> 1
        Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Engine!
        :param text: The text to encode
        :param default: The default value to encode when the character found is not accepted by the encoder
        """
        return self.encoder.encode(text, default=default)

    def decode(self, encoded_text: str | int | list) -> str:
        """
        Decode a text. For example: 1 -> A
        Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Engine!
        :param encoded_text: The text to decode
        """
        if type(encoded_text) == list:
            return self.encoder.decode(encoded_text[0])
        else:
            return self.encoder.decode(encoded_text)

    def encode_list(self, data: list, default: str = " ") -> str:
        """
        Encode a Python List
        :param data: The list to encode
        :param default: The default value to encode when the character found is not accepted by the encoder
        """
        return self.encoder.encode_list(data, default=default)

    def decode_list(self, encoded_data: str | int | list) -> list:
        """
        Decode a Python List
        :param encoded_data: The data to be decoded
        """
        if type(encoded_data) == list:
            return self.encoder.decode_list(encoded_data[0])
        else:
            return self.encoder.decode_list(encoded_data)

    def create_cloud_event(self) -> CloudEvents:
        """
        Create a Cloud Event
        """
        return self._event
