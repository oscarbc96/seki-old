import os
from shutil import which
from sys import exit

import click

from seki.__version__ import __version__
from seki.commands.build import _build
from seki.commands.cron import _cron
from seki.commands.drone import _drone
from seki.commands.repo import _repo
from seki.commands.run import _run
from seki.commands.template import _template


def check_requirements():
    ok = True

    requirements = ["git"]

    for requirement in requirements:
        if which(requirement) is None:
            ok = False
            click.echo(f"Missing tool: {requirement}")

    env_vars = ["DRONE_SERVER", "DRONE_TOKEN", "SEKI_PROJECT_OWNER", "SEKI_PROJECT_REPO"]

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


cli.add_command(_repo)
cli.add_command(_drone)
cli.add_command(_cron)
cli.add_command(_build)
cli.add_command(_run)
cli.add_command(_template)

if __name__ == "__main__":
    cli()
