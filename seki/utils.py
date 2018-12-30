import os
from getpass import getpass
from shutil import which
from sys import exit


def ask(title, options=None):
    if options:
        print(title)
        for idx, option in enumerate(options):
            print(f"[{idx+1}] {option}")

        options_length = len(options)

        choice = None
        while not choice:
            val = input("Enter option number: ")
            try:
                choice = int(val)

                if not 1 <= choice <= options_length:
                    print(f"Must be between 1 and {options_length}")
                    choice = None
            except ValueError:
                print("Must be a number")
        return choice
    else:
        return input(title)


def find_in_environ_or_ask(variable):
    if variable in os.environ:
        return os.environ[variable]
    else:
        question = variable + ":"
        if "password" in variable.lower():
            return getpass(question)
        else:
            return input(question)


def check_requirements():
    ok = True

    requirements = [
        "git",
        "drone"
    ]

    for requirement in requirements:
        if which(requirement) is None:
            ok = False
            print(f"Missing tool: {requirement}")

    env_vars = [
        "DRONE_SERVER",
        "DRONE_TOKEN"
    ]

    for var in env_vars:
        if var not in os.environ:
            ok = False
            print(f"Missing environment variable: {var}")

    if not ok:
        print("Exiting...")
        exit()
