import click

from seki.utils.drone import Drone


@click.command("drone", short_help="Activates drone.")
def _drone():
    if not Drone().is_enabled():
        Drone().enable_repository()
        click.echo("Seki project enabled in Drone.")
    else:
        click.echo("Seki project already enabled in Drone.")
