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
