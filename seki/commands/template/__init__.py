import click

from .template import get_template_params, get_params_values, process_template
from ...commands.shared import prepare_project, commit_changes
from ...conf import DRONE_PATH


@click.command("template", short_help="Generate drone from template.")
@click.argument("file", type=click.Path(exists=True))
@click.option("--cron", type=click.Choice(["@hourly", "@daily", "@weekly", "@monthly", "@yearly"]))
def cli(file, cron):
    prepare_project(cron)

    params = get_template_params(file)

    replacements = get_params_values(params)

    process_template(file, DRONE_PATH, replacements)

    commit_changes()
