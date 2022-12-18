"""
The Cloud Requests File
Inspired by @TimMcCool's scratchattach
"""

import time
import traceback
from threading import Thread

from scratchconnect import Warnings
from scratchconnect.CloudConnection import CloudConnection
from scratchconnect.scImage import Image

VERSION = "1.0 (beta)"
RESPONSE_VARIABLES = [f"Response_{i}" for i in range(1, 9)]
cloud_variable_length_limit = 256
FAIL = 0
SUCCESS = 1


class CloudRequests:
    def __init__(self, project_id, client_username, csrf_token, session_id, token, handle_all_errors,
                 print_logs, default=" "):
        print(f"[33m[1mScratchConnect [36mCloudRequests [37m- [35mv{VERSION}[3m[0m")
        self.t = None
        self.run_thread = False
        self.handle_all_errors = handle_all_errors
        self._request_functions = {}
        self._event_functions = {}
        self.print_logs = print_logs
        self.default = default
        self.cloud = CloudConnection(project_id=project_id,
                                     client_username=client_username,
                                     csrf_token=csrf_token,
                                     session_id=session_id, token=token)
        self._response_info_prev_value = self.cloud.get_cloud_variable_value("Response_Info", 10)[0]
        self._REQUESTS = []
        self._request = {}

    def request(self, req_name):
        """
        Decorator
        """

        def wrapper(func):
            self._request_functions[req_name] = func

        return wrapper

    def event(self, n):
        """
        Decorator
        """

        def wrapper(func):
            self._event_functions[n] = func

        return wrapper

    def emit(self, f_type, arguments="", t="request"):
        """
        Don't use this!
        """
        if t == "request":
            func = self._request_functions[f_type]
            if len(arguments) > 0:
                if len(arguments) == 1:
                    return func(arguments[0])
                else:
                    return func(*tuple(arguments))
            else:
                return func()
        else:
            if f_type in self._event_functions.keys():
                func = self._event_functions[f_type]
                func()

    def _done_request(self):
        """
        Don't use this!
        """
        self.get_request()
        self._REQUESTS = self.cloud.decode_list(self._request_value)
        self._REQUESTS.pop(0)
        self._set_cloud_variable("Request", self.cloud.encode_list(self._REQUESTS))
        time.sleep(1)

    def _set_cloud_variable(self, n, v):
        """
        Don't use this!
        """
        self.cloud.set_cloud_variable(variable_name=n, value=v)

    def _set_response_info(self, id, status_code, rv="", length=0, i=None):
        """
        Don't use this!
        """
        if i is None:
            i = []
        self._set_cloud_variable("Response_Info", self.cloud.encode_list([id, status_code, length, rv, *i]))

    def _get_response_info(self):
        """
        Don't use this!
        """
        return self.cloud.get_cloud_variable_value("Response_Info", 10)[0]

    def get_request(self):
        """
        Don't use this!
        """
        try:
            self._request_value = self._get_cloud_variable_value(variable_name="Request")[0]
        except IndexError:
            pass

    def _get_cloud_variable_value(self, variable_name, limit=100):
        """
        Don't use this!
        """
        if str(variable_name.strip())[0] != "☁":
            n = f"☁ {variable_name.strip()}"
        else:
            n = f"{variable_name.strip()}"
        data = []
        d = self.cloud.get_variable_data(limit=limit)
        i = 0
        while i < len(d):
            if d[i]['Name'] == n:
                data.append(d[i]['Value'])
                self._request["User"] = d[i]["User"]
                self._request["Timestamp"] = d[i]["Timestamp"]
            i = i + 1
        return data

    def _wait_for_ri_value_change(self):
        """
        Don't use this!
        """
        max_tries = 30
        tries = 0
        while True:
            current_value = self._get_response_info()
            if current_value != self._response_info_prev_value:
                self._response_info_prev_value = current_value
                return True
            tries += 1
            if tries >= max_tries:
                return False
            time.sleep(0.1)

    def _get_all_response_vars_value(self, max_length):
        """
        Don't use this!
        """
        value = ""
        data = self.cloud.get_variable_data(limit=1000)
        variables = [f"Response_{i}" for i in range(1, 9)]
        for var in variables:
            for i in data:
                if i["Name"].replace("☁ ", "") == var:
                    value += i["Value"]
                    break
            if len(value) >= max_length:
                break
        return value
        # variables = [f"Response_{i}" for i in range(1, 9)]
        # value = ""
        # for var in variables:
        #     v = self.cloud.get_cloud_variable_value(var, 50)[0]
        #     value += v
        #     print(var, " -> ", v)
        #     if len(value) >= max_length:
        #         break
        # return value

    def get_request_data(self):
        """
        Don't use this!
        """
        return self._request

    def _event(self, up):
        """
        Don't use this!
        """
        while self.run_thread:
            try:
                self.get_request()
                if self._request_value != "":
                    args = ""
                    n = 0
                    time.sleep(0.1)
                    while True:
                        try:
                            self._REQUESTS = self.cloud.decode_list(self._request_value)
                            request = self._REQUESTS[0]
                            req_id, req_name = self.cloud.decode_list(request)
                            self._request["Request ID"] = req_id
                            self._request["Request Name"] = req_name
                            _raw_ri = self._get_response_info()
                            ri = self.cloud.decode_list(_raw_ri)
                            self._log(message=
                                      f"[33m[1mScratchConnect [36mCloudRequests: [3m[38;2;255;255;255mNew Request: [37mID - [35m{req_id} [37mName - [35m{req_name}[0m")
                            if ri[0] == req_id:
                                _raw_d = ""
                                current_length = 0
                                data_length = int(ri[1])
                                self._set_cloud_variable("Response_Info", 1)
                                self._response_info_prev_value = "1"
                                while (data_length != current_length) or (data_length < current_length):
                                    if self._wait_for_ri_value_change():
                                        ri = self.cloud.decode_list(self._response_info_prev_value)
                                        if ri[0] == req_id and ri[1] == "Success":
                                            try:
                                                time.sleep(0.1)
                                                _raw_d += self._get_all_response_vars_value(max_length=int(ri[2]))
                                                current_length = len(_raw_d)
                                                if (current_length == data_length) or (data_length < current_length):
                                                    self._set_cloud_variable("Response_Info", 1)
                                                    self._response_info_prev_value = "1"
                                                    time.sleep(0.1)
                                                    break
                                            except IndexError:
                                                _raw_d += ""
                                            time.sleep(0.1)
                                            self._set_cloud_variable("Response_Info", 1)
                                            self._response_info_prev_value = "1"
                                args = self.cloud.decode_list(_raw_d)
                                self._request["Arguments"] = args
                                time.sleep(0.1)
                                self._set_cloud_variable("Response_Info", 1)
                                self._log(message=
                                          f"[33m[1mScratchConnect [36mCloudRequests: [37mID - [35m{req_id} [37mArguments - [35m{args}[0m")
                                break
                            else:
                                break
                        except (ValueError, IndexError) as E:
                            self.get_request()
                        n += 1
                        if n >= 3:
                            self._done_request()
                            break
                        time.sleep(0.1)
                    if n >= 3:
                        continue
                    self.emit("new_request", t="event")
                    if req_name in self._request_functions.keys():
                        return_value = self.emit(req_name, args)
                        encoded_value = ""
                        rv = ""
                        if type(return_value) is list:
                            data = return_value
                            rv = "List"
                            encoded_value = self.cloud.encode_list(data, default=self.default)
                        elif type(return_value) is dict:
                            data = list(return_value.values())
                            rv = "List"
                            encoded_value = self.cloud.encode_list(data, default=self.default)
                        elif (type(return_value) is str) or (return_value is None):
                            data = str(return_value)
                            rv = "String"
                            encoded_value = self.cloud.encode(data, default=self.default)
                        elif type(return_value) is int:
                            data = return_value
                            rv = "Int"
                            encoded_value = str(data)
                        elif type(return_value) == Image:
                            if return_value.encode_image():
                                data = return_value.get_image_data()
                                rv = "Image"
                                encoded_value = data
                            else:
                                Warnings.warn(
                                    f"[1m[33mScratchConnect [36mCloudRequests: [37mRequest ID - {req_id}: [31mClosing the request as the image data was invalid or cannot be found![0m")
                                self.emit("error", t="event")
                                self._set_response_info(req_id, FAIL)
                                self._done_request()
                                continue
                        splitted_data = self._split_encoded_data(encoded_value)
                        index = 0
                        variable_index = 0
                        l = len(encoded_value)
                        time.sleep(0.1)
                        if rv == "Image":
                            self._set_response_info(req_id, SUCCESS, rv, l, return_value.get_size())
                        else:
                            self._set_response_info(req_id, SUCCESS, rv, l)
                        success = True
                        while index < len(splitted_data):
                            self._set_cloud_variable(RESPONSE_VARIABLES[variable_index], splitted_data[index])
                            index += 1
                            variable_index += 1
                            wait = 0
                            if variable_index >= len(RESPONSE_VARIABLES):
                                variable_index = 0
                                self._set_response_info(req_id, SUCCESS)
                                while True:
                                    wait += 1
                                    if int(self._get_response_info()) == 1:
                                        break
                                    if wait >= 15:
                                        success = False
                                        Warnings.warn(
                                            f"[1m[33mScratchConnect [36mCloudRequests: [37mRequest ID - {req_id}: [31mClosing the request as the server didn't received a response form the Project! Maybe the project was stopped or closed![0m")
                                        self.emit("error", t="event")
                                        break
                                    time.sleep(0.1)
                            if wait >= 15:
                                break
                            time.sleep(0.1)
                        if success:
                            self._set_response_info(req_id, SUCCESS)
                            self._log(
                                message=f"[33m[1mScratchConnect [36mCloudRequests: [3m[32mSuccess: [37mID - [35m{req_id}[0m")
                    else:
                        self._log(
                            message=f"[33m[1mScratchConnect [36mCloudRequests: [3m[37mID - [35m{req_id}: [31mClosing the request as the return data was not found or the request name is invalid![0m")
                        self.emit("error", t="event")
                    self._done_request()
                time.sleep(up)
            except Exception as E:
                if E == "KeyBoardInterrupt":
                    self.run_thread = False
                Warnings.warn(f"[1m[33mScratchConnect: [37mError in Cloud Requests: [31m{E}:[0m")
                self.emit("error", t="event")
                self._done_request()
                if self.handle_all_errors:
                    print("[31m\t" + traceback.format_exc().replace("\n", "\n\t") + "[0m")
                else:
                    raise Exception(E)

    def _log(self, t="success", message=""):
        """
        Don't use this!
        """
        if self.print_logs:
            if t == "success":
                print(message)
            else:
                print(f"[1m[33mScratchConnect: [37mError in Cloud Requests: {message}")

    def _split_encoded_data(self, data):
        """
        Don't use this!
        """
        result = []
        i = 0
        temp_str = ""
        while i < len(data):
            temp_str += data[i]
            if len(temp_str) >= cloud_variable_length_limit:
                result.append(temp_str)
                temp_str = ""
            i += 1
        if len(temp_str) > 0:
            result.append(temp_str)
        while (len(result) % len(RESPONSE_VARIABLES)) != 0:
            result.append("")
        return result

    def get_request_info(self):
        """
        Get the request info
        """
        return self._request

    def start(self, update_time=1):
        """
        Start the events loop
        :param update_time: The update time
        """
        self.run_thread = True
        self.t = Thread(target=self._event, args=(update_time,))
        self.t.start()
        self.emit("connect", t="event")

    def stop(self):
        """
        Stop the events loop
        """
        self.run = False
