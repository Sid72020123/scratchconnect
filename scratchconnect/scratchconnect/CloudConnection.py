"""
The Cloud Variables File.
Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Encode/Decode Engine!
"""
import json
import requests
import websocket
import time
from pyemitter import Emitter
from threading import Thread

from scratchconnect import Exceptions
from scratchconnect.scEncoder import Encoder

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class CloudConnection:
    def __init__(self, project_id, client_username, csrf_token, session_id, token):
        """
        Main class to connect cloud variables
        """
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
        self.encoder = Encoder()
        self.event = Emitter()

    def get_variable_data(self, limit=100, offset=0):
        """
        Returns the cloud variable data
        :param limit: The limit
        :param offset: The offset or the number of values you want to skip from the beginning
        """
        response = requests.get(
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

    def get_cloud_variable_value(self, variable_name, limit=100):
        """
        Returns the cloud variable value
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

    def set_cloud_variable(self, variable_name, value):
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
        except ConnectionAbortedError or BrokenPipeError:
            self._make_connection()
            time.sleep(0.1)
            self.set_cloud_variable(variable_name, value)
            return False

    def encode(self, text):
        """
        Encode a text. For example: A -> 1
        Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Engine!
        :param text: The text to encode
        """
        return self.encoder.encode(text)

    def decode(self, encoded_text):
        """
        Decode a text. For example: 1 -> A
        Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Engine!
        :param encoded_text: The text to decode
        """
        return self.encoder.decode(encoded_text)

    def encode_list(self, data):
        """
        Encode a Python List
        :param data: The list
        """
        return self.encoder.encode_list(data)

    def decode_list(self, encoded_data):
        """
        Decode a Python List
        :param encoded_data: The data to be decoded
        """
        return self.encoder.decode_list(encoded_data)

    def _event(self, up):
        """
        This feature was requested by @Ankit_Anmol on Scratch
        """
        data = ""
        while True:
            live_data = self.get_variable_data(limit=3)[0]
            if data != live_data:
                data = live_data
                self.event.emit('change', user=data['User'], action=data['Action'],
                                variable_name=data['Name'], value=data['Value'],
                                timestamp=data['Timestamp'])
            time.sleep(up)

    def start_event(self, update_time=1):
        """
        This feature was requested by @Ankit_Anmol on Scratch
        """
        Thread(target=self._event, args=(update_time,)).start()
