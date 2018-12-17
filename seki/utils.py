import os
from getpass import getpass


def find_in_environ_or_ask(variable):
    if variable in os.environ:
        return os.environ[variable]
    else:
        question = variable + ":"
        if "password" in variable.lower():
            return getpass(question)
        else:
            return input(question)
