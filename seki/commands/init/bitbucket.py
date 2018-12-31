import click
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import (
    Repository,
    RepositoryPayload,
    RepositoryForkPolicy
)
from requests.exceptions import HTTPError

from ...conf import REPOSITORY_PATH
from ...utils.git_cli import clone_repo


def find_bitbucket_repository(email, user, password):
    bitbucket = Client(
        BasicAuthenticator(user, password, email)
    )

    try:
        click.echo("Finding seki project in bitbucket...")
        repository = Repository.find_repository_by_name_and_owner(
            repository_name="seki",
            client=bitbucket
        )
    except HTTPError:
        click.echo("Project not found")
        click.echo("Creating project seki...")

        repository = Repository.create(
            payload=RepositoryPayload({
                "name": "seki",
                "is_private": True,
                "fork_policy": RepositoryForkPolicy.NO_FORKS,
            }),
            client=bitbucket
        )

    for link in repository.links["clone"]:
        if link["name"] == "https":
            return link["href"]


@click.command("bitbucket")
@click.option("--user", prompt=True)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def command(email, user, password):
    clone_url = find_bitbucket_repository(email, user, password)

    clone_repo(clone_url, REPOSITORY_PATH)
