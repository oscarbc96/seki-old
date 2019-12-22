from os.path import exists

import click
from git import Repo

from seki.conf import REPOSITORY_PATH


@click.group("repo", short_help="Initializes the repo.")
def _repo():
    pass


@_repo.command("clone")
@click.argument("clone_url")
def _clone(clone_url):
    if exists(REPOSITORY_PATH):
        click.echo("Seki project already exists.")
    else:
        click.echo(f"Clonning project from {clone_url} into {REPOSITORY_PATH}")
        Repo.clone_from(clone_url, REPOSITORY_PATH)
