import click
import yaml

from seki.commands.shared import commit_changes, prepare_project
from seki.conf import DRONE_PATH


@click.command("run", short_help="Quick run tool in pipeline.")
@click.argument("image")
@click.option("--args", help="Arguments for docker image.")
@click.option("--telegram", is_flag=True, help="Notify on telegram build result.")
@click.option("--cron", help="Cron expression.")
def _run(image, args, telegram, cron):
    prepare_project(cron)

    drone_yml = generate_drone_yml(image, args, telegram)

    dump_drone_yml(DRONE_PATH, drone_yml)

    commit_changes()


def generate_drone_yml(image, args, telegram):
    click.echo("Generating new 'drone.yml' from args...")

    template = {
        "kind": "pipeline",
        "name": "default",
        "clone": {"disable": True},
        "steps": [],
    }

    run_step = {
        "name": "run",
        "image": image,
    }

    if args:
        run_step["commands"] = [args]

    template["steps"].append(run_step)

    if telegram:
        template["steps"].append({"name": "create tar", "image": "alpine", "commands": ["tar czf output.tar.gz ."]})

        template["steps"].append(
            {
                "name": "telegram notificaton",
                "image": "appleboy/drone-telegram",
                "settings": {
                    "token": {"from_secret": "telegram_token"},
                    "to": {"from_secret": "telegram_to"},
                    "format": "markdown",
                    "message": """
                    {{#success build.status}}
                        {{build.number}}: ✅ `{{commit.message}}` 🚁 [See build]({{build.link}})
                    {{else}}
                        {{build.number}}: ❌ `{{commit.message}}` 🚁 [See build]({{build.link}})
                    {{/success}}
                """,
                    "document": ["output.tar.gz"],
                },
            }
        )

    return template


def dump_drone_yml(drone_path, template):
    click.echo(f"Dumping content to '{drone_path}'")

    with open(drone_path, "w") as drone_yml:
        yaml.dump(template, drone_yml, default_flow_style=False)
