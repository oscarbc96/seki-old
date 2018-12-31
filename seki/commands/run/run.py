import click
import yaml


def generate_drone_yml(image, args, telegram):
    click.echo("Generating new 'drone.yml' from args...")

    template = {
        "kind": "pipeline",
        "name": "default",
        "clone": {
            "disable": True
        },
        "steps": []
    }

    run_step = {
        "name": "run",
        "image": image,
    }

    if args:
        run_step["commands"] = [args]

    template["steps"].append(run_step)

    if telegram:
        template["steps"].append({
            "name": "create tar",
            "image": "alpine",
            "commands": [
                "tar czf output.tar.gz ."
            ]
        })

        template["steps"].append({
            "name": "telegram notificaton",
            "image": "appleboy/drone-telegram",
            "settings": {
                "token": {
                    "from_secret": "telegram_token"
                },
                "to": {
                    "from_secret": "telegram_to"
                },
                "format": "markdown",
                "message": """
                    {{#success build.status}}
                        {{build.number}}: ✅ `{{commit.message}}` 🚁 [See build]({{build.link}})
                    {{else}}
                        {{build.number}}: ❌ `{{commit.message}}` 🚁 [See build]({{build.link}})
                    {{/success}}
                """,
                "document": [
                    "output.tar.gz"
                ]
            }
        })

    return template


def dump_drone_yml(drone_path, template):
    click.echo("Dumping content to 'drone.yml'")

    drone_yml = open(drone_path, "w")

    yaml.dump(template, drone_yml, default_flow_style=False)

    drone_yml.close()
