import click

from .run import generate_drone_yml, dump_drone_yml
from ...commands.shared import prepare_project, commit_changes
from ...conf import DRONE_PATH


@click.command("run", short_help="Quick run tool in pipeline.")
@click.argument("image")
@click.option("--args", help="Arguments for docker image.")
@click.option("--telegram", is_flag=True, help="Notify on telegram build result.")
@click.option("--cron", type=click.Choice(["@hourly", "@daily", "@weekly", "@monthly", "@yearly"]))
def cli(image, args, telegram, cron):
    prepare_project(cron)

    drone_yml = generate_drone_yml(image, args, telegram)

    dump_drone_yml(DRONE_PATH, drone_yml)

    commit_changes()
