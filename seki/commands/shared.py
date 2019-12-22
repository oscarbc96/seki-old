import sys
from datetime import datetime

from seki.conf import DRONE_PATH
from seki.utils.drone import Drone
from seki.utils.encodings import md5, string_to_b64
from seki.utils.git_cli import checkout, commit, create_branch, get_repo, push


def get_input_args():
    return " ".join(sys.argv[1:])


def get_input_args_and_timestamp():
    return get_input_args() + " - " + datetime.now().isoformat()


def prepare_project(cron):
    repo = get_repo()

    checkout(repo, "master")

    if cron:
        branch_name_encoded = string_to_b64(get_input_args_and_timestamp())

        create_branch(repo, branch_name_encoded)

        Drone().cron_create(md5(branch_name_encoded), cron, branch_name_encoded)


def append_header_to_drone_yml(header):
    header = "# " + header + "\n"

    drone_yml = open(DRONE_PATH, "r+")

    body = drone_yml.read()

    drone_yml.seek(0)

    drone_yml.write(header + body)

    drone_yml.close()


def commit_changes():
    input_args = get_input_args_and_timestamp()

    append_header_to_drone_yml(input_args)

    repo = get_repo()

    commit_hash = commit(repo, input_args)

    push(repo)

    return commit_hash
