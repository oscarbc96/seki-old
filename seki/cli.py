import os
from shutil import which
from sys import exit

import click

from .__version__ import __version__
from .commands.drone import cli as drone
from .commands.init import cli as init
from .commands.run import cli as run
from .commands.template import cli as template


def check_requirements():
    ok = True

    requirements = [
        "git",
        "drone"
    ]

    for requirement in requirements:
        if which(requirement) is None:
            ok = False
            click.echo(f"Missing tool: {requirement}")

    env_vars = [
        "DRONE_SERVER",
        "DRONE_TOKEN"
    ]

    for var in env_vars:
        if var not in os.environ:
            ok = False
            click.echo(f"Missing environment variable: {var}")

    if not ok:
        click.echo("Exiting...")
        exit()


@click.group()
@click.version_option(prog_name="seki", version=__version__)
def cli():
    check_requirements()


cli.add_command(init)
cli.add_command(drone)
cli.add_command(run)
cli.add_command(template)

if __name__ == "__main__":
    cli()
