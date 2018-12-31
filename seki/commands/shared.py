import sys
from datetime import datetime
from hashlib import md5

import click

from ..conf import DRONE_PATH
from ..utils.drone import run as run_drone
from ..utils.git_cli import get_repo, commit, push, create_branch, checkout, get_repo_path_from_origin


def generate_header():
    current_time = datetime.now().isoformat(" ", "seconds")

    args = " ".join(sys.argv)

    return args + " - " + current_time


def add_drone_cron(repository, branch, cron_expr):
    click.echo("Creating cron job in drone...")

    result = run_drone([
        "cron",
        "add",
        "--branch",
        branch,
        repository,
        branch,  # name for cron
        cron_expr
    ])

    if result != "":
        click.echo("Not able to activate repository in drone")


def prepare_project(cron):
    repo = get_repo()

    checkout(repo, "master")

    if cron:
        branch_name = generate_header()

        branch_name_hash = md5(branch_name.encode("utf-8")).hexdigest()

        create_branch(repo, branch_name_hash)

        checkout(repo, branch_name_hash)

        repo_path = get_repo_path_from_origin(repo)

        add_drone_cron(repo_path, branch_name_hash, cron)


def append_header_to_drone_yml(header):
    header = "# " + header + "\n"

    drone_yml = open(DRONE_PATH, "r+")

    body = drone_yml.read()

    drone_yml.seek(0)

    drone_yml.write(header + body)

    drone_yml.close()


def commit_changes():
    header = generate_header()

    append_header_to_drone_yml(header)

    repo = get_repo()

    commit(repo, header)

    push(repo)
