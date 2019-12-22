from datetime import datetime

import click
from tabulate import tabulate

from seki.utils.drone import Drone
from seki.utils.encodings import b64_to_str


@click.group("cron", short_help="Manage cron jobs.")
def _cron():
    pass


@_cron.command("list", short_help="List cron jobs.")
def _list():
    cron_jobs = Drone().cron_list()
    if cron_jobs:
        click.echo(
            tabulate(
                [
                    {
                        "Name": cron["name"],
                        "Next": datetime.utcfromtimestamp(cron["next"]).isoformat() if cron["next"] else "N/A",
                        "Previous": datetime.utcfromtimestamp(cron["prev"]).isoformat() if cron["prev"] else "N/A",
                        "Branch": b64_to_str(cron["branch"]),
                    }
                    for cron in cron_jobs
                ],
                headers="keys",
            )
        )
    else:
        click.echo("Cron job list empty.")


@_cron.command("delete", short_help="Delete cron job.")
@click.argument("cron_names", nargs=-1)
def _delete(cron_names):
    for cron_name in cron_names:
        Drone().cron_delete(cron_name)
        click.echo(f"Removed cron: {cron_name}")
