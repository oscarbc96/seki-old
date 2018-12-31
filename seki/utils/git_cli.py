from urllib.parse import urlparse

import click
from git import Repo

from ..conf import REPOSITORY_PATH


def get_repo():
    return Repo(REPOSITORY_PATH)


def clone_repo(clone_url, folder):
    click.echo("Clonning repo...")
    return Repo.clone_from(clone_url, folder)


def create_branch(repo, branch_name):
    click.echo(f"Creating new branch '{branch_name}'...")
    repo.git.reset("--hard")

    repo.git.checkout("-b", branch_name)


def checkout(repo, branch_name):
    repo.git.reset("--hard")

    repo.git.checkout(branch_name)


def commit(repo, message):
    repo.git.add("--all")

    repo.git.commit(m=message)

    short_sha = repo.head.object.hexsha[:7]

    click.echo(f"Commit: '{short_sha}'")


def push(repo):
    click.echo("Pushing changes...")
    branch = repo.active_branch.name
    if branch != "master":
        repo.git.push("origin", branch)
    else:
        repo.git.push()


def get_repo_path_from_origin(repo):
    repo_url = repo.remotes.origin.url
    path = urlparse(repo_url).path
    path = path.rsplit(".", 1)[0]

    if path.startswith("/"):
        path = path[1:]

    return path
