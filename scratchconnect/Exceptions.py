class InvalidInfo(Exception):
    """
    Raised when the username or password is invalid
    """
    pass


class InvalidUser(Exception):
    """
    Raised when the username is invalid
    """
    pass


class InvalidStudio(Exception):
    """
    Raised when the studio is invalid
    """
    pass


class InvalidProject(Exception):
    """
    Raised when the project is invalid
    """
    pass


class UnauthorizedAction(Exception):
    """
    Raised when the action is unauthorized
    """
    pass


class InvalidCloudValue(Exception):
    """
    Raised when the cloud value is invalid
    """
    pass


class InvalidForumTopic(Exception):
    """
    Raised when the forum topic is invalid
    """
    pass
