import click

from ...utils.drone import run
from ...utils.git_cli import get_repo, get_repo_path_from_origin


def is_enabled(repository):
    click.echo("Check if drone is enabled...")

    result = run([
        "repo",
        "info",
        repository,
        "--format",
        "{{.Active}}"
    ])

    return "true" in result


def enable_repository(repository):
    click.echo("Enabling drone...")
    # Drone sync
    result = run([
        "repo",
        "sync"
    ])

    if repository not in result:
        click.echo("Drone sync failed")
        exit()

    # Enable project
    result = run([
        "repo",
        "enable",
        repository
    ])

    if "Successfully activated repository" not in result:
        click.echo("Not able to activate repository in drone")
        exit()


@click.command("drone", short_help="Activates drone.")
def cli():
    repo = get_repo()

    repo_path = get_repo_path_from_origin(repo)

    if not is_enabled(repo_path):
        enable_repository(repo_path)
    else:
        click.echo("Drone already enabled.")
