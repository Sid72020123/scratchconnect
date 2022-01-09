"""
The Cloud Storage File.
"""
import time
import json
import string
from threading import Thread

from scratchconnect.CloudConnection import CloudConnection
from scratchconnect.scEncoder import Encoder

SUPPORTED_CHARS = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation + ' ')
_VARIABLE_LENGTH = 256
_VARIABLES = ['Response1', 'Response2', 'Response3', 'Response4', 'Response5', 'Response6', 'Response7', 'Response8']

_FAIL = 0
_SUCCESS = 1
_ACCESS_DENIED = 2
_ALREADY_EXIST = 3
_DOESNT_EXIST = 4


class CloudStorage:
    def __init__(self, file_name, rewrite_file, project_id, client_username, csrf_token, session_id, token,
                 edit_access):
        self.project_id = project_id
        self.client_username = client_username
        self.csrf_token = csrf_token
        self.session_id = session_id
        self.token = token
        self.file_name = f"{file_name}.json"
        self.rewrite_file = rewrite_file
        self._make_file()
        self.edit_access = edit_access
        self.edit_access.append(client_username)
        self._connect_cloud()
        self.encoder = Encoder()
        self.loop = True

    def _connect_cloud(self):
        self.cloud = CloudConnection(self.project_id, self.client_username, self.csrf_token, self.session_id,
                                     self.token)

    def _get_request(self):
        return self._get_cloud_variable_data('Request')[0]

    def _reset_request_var(self):
        try:
            self.cloud.set_cloud_variable(variable_name='Request', value=0)
        except:  # lgtm [py/catch-base-exception]
            time.sleep(1)
            self._connect_cloud()

    def _set_response_info(self, status_code):
        try:
            self.cloud.set_cloud_variable(variable_name='Response Info',
                                          value=self.encoder.encode_list([status_code]))
        except:  # lgtm [py/catch-base-exception]
            time.sleep(1)
            self._connect_cloud()

    def _set_cloud_var(self, name, value):
        try:
            return self.cloud.set_cloud_variable(variable_name=name, value=value)
        except:  # lgtm [py/catch-base-exception]
            time.sleep(1)
            self._connect_cloud()

    def start_cloud_loop(self, update_time=5, print_requests=False):
        t = Thread(target=self._start_loop, args=(update_time, print_requests,))
        t.start()

    def _start_loop(self, update_time, pr):
        while self.loop:
            try:
                if pr:
                    print("Checking for new request...")
                r = self._get_request()
                request = self.encoder.decode_list(str(r[0]))
                if len(request) > 1:
                    request_type = request[0]
                    request_name = request[1]
                    if request_name == "":
                        request_name = None
                    user = r[1]
                    if pr:
                        print('-' * 30)
                        print(f"New Request {request_type}:")
                        print(f"\tType: {request_type}")
                        print(f"\tName: {request_name}")
                        print(f"\tUser: {user}")
                        print('-' * 30)
                    if request_type == "CREATE":
                        if user in self.edit_access:
                            file = self._open_file(mode='r+')
                            data = json.loads(file.read())
                            file.close()
                            if request_name in data:
                                self._set_response_info(status_code=_ALREADY_EXIST)
                                self._reset_request_var()
                                continue
                            else:
                                data[request_name] = 0
                            file = self._open_file(mode='w')
                            file.write(json.dumps(data))
                            file.close()
                            self._set_response_info(status_code=_SUCCESS)
                            self._reset_request_var()
                            if pr:
                                print(f"{request_type} - {request_name} Success!")
                        else:
                            self._set_response_info(status_code=_ACCESS_DENIED)
                            self._reset_request_var()

                    if request_type == "DELETE":
                        if user in self.edit_access:
                            file = self._open_file(mode='r+')
                            data = json.loads(file.read())
                            file.close()
                            if request_name not in data:
                                self._set_response_info(status_code=_DOESNT_EXIST)
                                self._reset_request_var()
                                continue
                            else:
                                del data[request_name]
                            file = self._open_file(mode='w')
                            file.write(json.dumps(data))
                            file.close()
                            self._set_response_info(status_code=_SUCCESS)
                            self._reset_request_var()
                            if pr:
                                print(f"{request_type} - {request_name} Success!")
                        else:
                            self._set_response_info(status_code=_ACCESS_DENIED)
                            self._reset_request_var()

                    if request_type == "DELETE_ALL":
                        if user in self.edit_access:
                            file = self._open_file(mode='w')
                            file.write(json.dumps({}))
                            file.close()
                            self._set_response_info(status_code=_SUCCESS)
                            self._reset_request_var()
                            if pr:
                                print(f"{request_type} - Success!")
                        else:
                            self._set_response_info(status_code=_ACCESS_DENIED)
                            self._reset_request_var()

                    if request_type == "GET":
                        d = self._get_data(request_name)
                        if d is None:
                            self._set_response_info(status_code=_DOESNT_EXIST)
                            self._reset_request_var()
                            continue
                        else:
                            data = self.encoder.encode(str(d))
                            divided_data = self._divide_code(data, _VARIABLE_LENGTH)
                            i = 0
                            while i < len(divided_data):
                                if divided_data[i] == '':
                                    if self._set_cloud_var(name=_VARIABLES[i], value='') is False:
                                        continue
                                else:
                                    if self._set_cloud_var(name=_VARIABLES[i], value=divided_data[i]) is False:
                                        continue
                                i += 1
                                time.sleep(0.5)
                            self._set_response_info(status_code=_SUCCESS)
                            self._reset_request_var()
                            if pr:
                                print(f"{request_type} - {request_name} Success!")

                    if request_type == "SET":
                        v = ""
                        i = 0
                        while i < len(_VARIABLES):
                            d = self.cloud.get_cloud_variable_value(_VARIABLES[i], limit=3)
                            if len(d) > 0:
                                v += d[0]
                            i += 1
                            time.sleep(0.1)
                        value = self.encoder.decode(v)
                        file = self._open_file(mode='r+')
                        data = json.loads(file.read())
                        file.close()
                        if request_name in data:
                            data[request_name] = value
                        else:
                            self._set_response_info(status_code=_DOESNT_EXIST)
                            self._reset_request_var()
                            continue
                        file = self._open_file(mode='w')
                        file.write(json.dumps(data))
                        file.close()
                        self._set_response_info(status_code=_SUCCESS)
                        self._reset_request_var()
                        if pr:
                            print(f"{request_type} - {request_name} Success!")

                time.sleep(update_time)
            except KeyboardInterrupt:
                pass

    def _make_file(self):
        if self.rewrite_file:
            file = open(self.file_name, 'w+')
        else:
            file = open(self.file_name, 'a+')
        t_file = open(self.file_name, 'r')
        if len(t_file.read()) == 0:
            file.write(json.dumps({}))
        t_file.close()
        file.close()

    def _open_file(self, mode='r'):
        file = open(self.file_name, mode)
        return file

    def _get_data(self, key):
        try:
            file = json.loads(self._open_file(mode='r').read())
            return file[key]
        except KeyError:
            return None

    def _get_cloud_variable_data(self, variable_name, limit=100):
        if str(variable_name.strip())[0] != "☁":
            n = f"☁ {variable_name.strip()}"
        else:
            n = f"{variable_name.strip()}"
        data = []
        d = self.cloud.get_variable_data(limit=limit)
        i = 0
        while i < len(d):
            if d[i]['Name'] == n:
                data.append([d[i]['Value'], d[i]['User']])
            i = i + 1
        return data

    def _divide_code(self, data, letters_length, list_length=8):
        i = 0
        divide = []
        text = ""
        while i < len(data):
            text += data[i]
            if len(text) >= letters_length:
                divide.append(text)
                text = ""
            i += 1
        if len(text) > 0:
            divide.append(text)
        while len(divide) < list_length:
            divide.append('')
        return divide
