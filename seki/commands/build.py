from datetime import datetime

import click
from tabulate import tabulate

from seki.conf import DRONE_PROJECT
from seki.utils.drone import Drone


@click.group("build", short_help="Manage builds.")
def _build():
    pass


@_build.command("list", short_help="List last 15 builds.")
def _list():
    builds = Drone().build_list()[:15]
    if builds:
        click.echo(
            tabulate(
                [
                    {
                        "Command": build["message"],
                        "Build": f"{DRONE_PROJECT}/{build['number']}",
                    }
                    for build in builds
                ],
                headers="keys",
            )
        )
    else:
        click.echo("Builds list empty.")
