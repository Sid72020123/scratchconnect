"""
The Turbowarp Cloud Variables File.
Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Encode/Decode Engine!
"""
import ssl  # Used if the Certificate is expired specially in Windows 10 machine
import json
import websocket
from ssl import SSLEOFError, SSLError

from scratchconnect import Exceptions
from scratchconnect.scEncoder import Encoder
from scratchconnect.scCloudEvents import CloudEvents

_website = "scratch.mit.edu"
_login = f"https://{_website}/login/"
_api = f"api.{_website}"


class TurbowarpCloudConnection:
    def __init__(self, project_id, username):
        """
        Main class to connect turbowarp cloud variables
        """
        self.project_id = project_id
        self.username = username
        self._cloud_d = None
        self._event = CloudEvents("Turbowarp", self)
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
        self._event.emit('connect')

    def get_variable_data(self) -> list:
        """
        Returns the cloud variable data
        """
        self.set_cloud_variable("@sc_temp", "123")
        data = []
        for d in self._cloud_d.split("\n"):
            one = json.loads(d)
            if one["name"] != "☁ @sc_temp":
                data.append(one)
        if len(data) == 0:
            return None
        return data

    def get_cloud_variable_value(self, variable_name: str, limit: int) -> list:
        value = []
        data = self.get_variable_data()
        for d in data:
            if d["name"] == f"☁ {variable_name}":
                value.append(d["value"])
        return value[0:limit]

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
                    "Turbowarp has Cloud Variable Limit of 256 Characters per variable. Try making the value shorter!")
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
            self._cloud_d = self._ws.recv()
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

    def decode(self, encoded_text: str | int) -> str:
        """
        Decode a text. For example: 1 -> A
        Go to https://scratch.mit.edu/projects/578255313/ for the Scratch Engine!
        :param encoded_text: The text to decode
        """
        return self.encoder.decode(encoded_text)

    def encode_list(self, data: list, default: str = " ") -> str:
        """
        Encode a Python List
        :param data: The list to encode
        :param default: The default value to encode when the character found is not accepted by the encoder
        """
        return self.encoder.encode_list(data, default=default)

    def decode_list(self, encoded_data: str | int) -> list:
        """
        Decode a Python List
        :param encoded_data: The data to be decoded
        """
        return self.encoder.decode_list(encoded_data)

    def create_cloud_event(self) -> CloudEvents:
        """
        Create a Cloud Event
        """
        return self._event
