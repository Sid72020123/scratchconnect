"""
Main File
"""

import json
from rich.console import Console
from rich.theme import Theme

_name = "Scratch Terminal"
_version = "v1.0"
_logo_style = "bold blue"
_version_style = "italic #ffffff"
_command = "[bold yellow]scratch> "
Commands = {
    "info": "Prints the Scratch Terminal Info",
    "help": "This help",
    "console_info": "Prints the info of your Console/Terminal",
    "news": "Prints Scratch News",
    "user <username>": "Prints Scratch User data",
    "studio <id>": "Prints Scratch Studio data",
    "project <id>": "Prints Scratch Project data",
}


class Terminal:
    def __init__(self, sc):
        """
        Main Terminal Class
        """
        self.sc = sc

    def start(self):
        """
        Start the loop
        """
        self.run = True
        self._start_loop()

    def _print_console_information(self):
        """
        Don't use this
        """
        data = {
            "Size": list(self.console.size),
            "Encoding": str(self.console.encoding),
            "Is Terminal?": str(self.console.is_terminal),
            "Color System": str(self.console.color_system)
        }
        self._print_data(data_type="Console", data=dict(data))

    def _error(self, message):
        """
        Don't use this
        """
        self.console.print(message, style="bold red")

    def _print_info(self):
        """
        Don't use this
        """
        self.console.rule("[bold red]Scratch Terminal Information")
        string = {
            "Name": _name,
            "Version": _version,
            "Description": "Scratch Terminal is a CLI Terminal programmed in Python to get the data of Scratch User, Studio, Project, etc. in the Terminal!",
            "Made By": "[blue underline]@Sid72020123[/] on [blue underline]Scratch[/]"
        }
        for i in string:
            self.console.print(i, style="bold cyan", end=": ")
            self.console.print(string[i], style="italic green")
        print()

    def _print_help(self):
        """
        Don't use this
        """
        self.console.rule("[bold red]Scratch Terminal Help")
        self.console.print("You can use the following Commands:", style="italic red")
        for i in Commands:
            self.console.print(i, style="bold cyan", end=": ")
            self.console.print(Commands[i], style="italic green")
        print()

    def _print_data(self, data_type, data):
        """
        Don't use this
        """
        self.console.rule(f"[bold red]{data_type} Information")
        for i in data:
            self.console.print(f"{i}:", style="bold cyan")
            if isinstance(data[i], str) and data_type in ["User", "Stduio", "Project"]:
                self.console.print(f"\t{data[i]}".replace("\n", "\n\t").title(), style="italic green")
            else:
                self.console.print(f"\t{data[i]}", style="italic green")
        print()

    def _get_sub_command(self, command):
        """
        Don't use this
        """
        try:
            result = command[1]
        except:
            self._error(f"The '{command[0]}' is missing some required arguments!")
            result = None
        return result

    def _start_loop(self):
        """
        Don't use this
        """
        self.console = Console(theme=Theme(inherit=False), soft_wrap=False)
        self.console.print(_name, style=_logo_style, end=" ")
        self.console.print(_version, style=_version_style)
        while self.run:
            user_input = self.console.input(_command)
            command_data = self._split_command(user_input)
            if len(command_data) <= 0:
                command = ""
            else:
                command = command_data[0]
            if command == "":
                pass
            elif command == "exit":
                self.console.print("Stopping Scratch Terminal...", style="bold red")
                self.run = False
                self.console.print("Successfully Stopped the Terminal!", style="bold red")
            elif command == "console_info":
                with self.console.status("Checking Console Information..."):
                    self._print_console_information()
            elif command == "info":
                self._print_info()
            elif command == "help":
                self._print_help()
            elif command == "news":
                with self.console.status("Fetching Scratch News..."):
                    data = self.sc.site_news()
                    news = {}
                    for item in data:
                        news[item["headline"]] = item["copy"]
                    self._print_data(data_type="News", data=news)
            elif command == "user":
                sub_command = self._get_sub_command(command_data)
                if sub_command is not None:
                    with self.console.status("Fetching User Data..."):
                        try:
                            user = self.sc.connect_user(sub_command)
                            data = user.all_data()
                        except:
                            data = None
                        if data is not None:
                            self._print_data(data_type="User", data=user.all_data())
                        else:
                            self._error("The Username is Invalid or some required data was not found about that user.")
            elif command == "studio":
                sub_command = self._get_sub_command(command_data)
                if sub_command is not None:
                    with self.console.status("Fetching Studio Data..."):
                        try:
                            studio = self.sc.connect_studio(sub_command)
                            data = studio.all_data()
                        except:
                            data = None
                        if data is not None:
                            self._print_data(data_type="Studio", data=studio.all_data())
                        else:
                            self._error(
                                "The Studio ID is Invalid or some required data was not found about that studio.")
            elif command == "project":
                sub_command = self._get_sub_command(command_data)
                if sub_command is not None:
                    with self.console.status("Fetching Project Data..."):
                        try:
                            project = self.sc.connect_project(sub_command)
                            data = project.all_data()
                        except:
                            data = None
                        if data is not None:
                            self._print_data(data_type="Project", data=project.all_data())
                        else:
                            self._error(
                                "The Project ID is Invalid or some required data was not found about that project.")
            else:
                self._error("Invalid Command!")

    def _split_command(self, text):
        """
        Don't use this
        """
        splitted_data = text.split(" ")
        result = []
        for item in splitted_data:
            if item != "":
                result.append(item.lower())
        return result
