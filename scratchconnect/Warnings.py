"""
The Warnings File
"""
import warnings


class CookieLoginWarning:
    def __init__(self, message):
        """
        Warned when a user logs in with cookie
        """
        warnings.warn(message)


class LoginWarning:
    def __init__(self, message):
        """
        Warned when a user fails to log-in
        """
        warnings.warn(message)
