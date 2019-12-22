import click
from git import Repo

from seki.conf import REPOSITORY_PATH


def get_repo():
    return Repo(REPOSITORY_PATH)


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

    return repo.head.object.hexsha


def push(repo):
    click.echo("Pushing changes...")
    repo.git.push("origin", repo.active_branch.name)
