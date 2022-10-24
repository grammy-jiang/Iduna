"""
The exceptions in this application
"""


class Aria2Exception(Exception):
    """
    the base exception
    """


class CommandNotFound(Aria2Exception):
    """
    the command of aria2c not found
    """
