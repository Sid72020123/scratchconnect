"""
The ScratchConnect Cloud Events Class
"""

import time
from threading import Thread


class CloudEvents:
    def __init__(self, cloud_object_type, cloud_object):
        self.t = None
        if cloud_object_type in ["Scratch", "Turbowarp"]:
            self.cloud_object_type = cloud_object_type
        else:
            raise TypeError("Invalid Cloud Type Provided!")
        self.cloud_object = cloud_object
        self._event_functions = {
            "connect": None,
            "create": None,
            "delete": None,
            "set": None,
            "disconnect": None
        }
        self.run = False

    def on(self, e_type):
        """
        Decorator
        """

        def wrapper(func):
            if e_type not in list(self._event_functions.keys()):
                raise TypeError(
                    f"Invalid Event Type '{e_type}'. Use only one from {list(self._event_functions.keys())}")
            else:
                self._event_functions[e_type] = func

        return wrapper

    def emit(self, e_type, **data):
        """
        Don't use this!
        """
        func = self._event_functions[e_type]
        if func is not None:
            if e_type in ['connect', 'disconnect']:
                func()
            else:
                func(data)

    def _event(self, up):
        """
        Don't use this!
        """
        data = ""
        while self.run:
            live_data = self.cloud_object.get_variable_data()[0]
            if data != live_data:
                data = live_data
                emit_action = ""
                if self.cloud_object_type == "Scratch":
                    action = data['Action'].split("_")[0]
                    if action == "set":
                        emit_action = "set"
                    elif action == "del":
                        emit_action = "delete"
                    elif action == "create":
                        emit_action = "create"
                elif self.cloud_object_type == "Turbowarp":
                    emit_action = data["method"]

                if self.cloud_object_type == "Scratch":
                    self.emit(emit_action, user=data['User'], action=data['Action'],
                              variable_name=data['Name'], value=data['Value'],
                              timestamp=data['Timestamp'])
                elif self.cloud_object_type == "Turbowarp":
                    self.emit(emit_action, action=data['method'],
                              variable_name=data['name'], value=data['value'])
            time.sleep(up)

    def start(self, update_time=1):
        """
        Start the events loop
        :param update_time: The update time
        """
        self.cloud_object._make_connection()
        self.run = True
        self.t = Thread(target=self._event, args=(update_time,))
        self.t.start()

    def stop(self):
        """
        Stop the events loop
        """
        self.run = False
