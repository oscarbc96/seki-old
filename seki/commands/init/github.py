import click
import requests

from requests.auth import HTTPBasicAuth

from ...conf import REPOSITORY_PATH
from ...utils.git_cli import clone_repo


@click.command("github")
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def command(username, password):
    payload = {
        "name": "seki",
        "private": True,
    }

    auth = HTTPBasicAuth(username, password)

    response = requests.post("https://api.github.com/user/repos", data=payload, auth=auth)

    if response.status_code != requests.codes.created:
        click.echo(response.text)

        click.echo("Try manual activation.")
    else:
        clone_url = f"git@github.com:{username}/seki.git"
        clone_repo(clone_url, REPOSITORY_PATH)
