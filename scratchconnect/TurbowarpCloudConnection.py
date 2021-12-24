"""
The Turbowarp Cloud Variables File.
Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Encode/Decode Engine!
"""
import ssl  # Used if the Certificate is expired specially in Windows 10 machine
import json
import time
import websocket

from scratchconnect import Exceptions
from scratchconnect.scEncoder import Encoder

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class TurbowarpCloudConnection:
    def __init__(self, project_id, username):
        """
        Main class to connect cloud variables
        """
        self.project_id = project_id
        self.username = username
        self._make_connection()
        self.encoder = Encoder()

    def _send_packet(self, packet):
        """
        Don't use this
        """
        self._ws.send(json.dumps(packet) + "\n")

    def _make_connection(self):
        """
        Don't use this
        """
        self._ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        self._ws.connect("wss://clouddata.turbowarp.org",
                         origin="https://turbowarp.org",
                         enable_multithread=True)
        self._send_packet(
            {
                "method": "handshake",
                "user": self.username,
                "project_id": str(self.project_id),
            }
        )

    def get_variable_data(self):
        """
        Returns the cloud variable data
        """
        data = json.loads(self._ws.recv())
        return data

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
                "user": self.username,
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
