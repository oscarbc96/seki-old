import re
import yaml


def get_template_params(template_path):
    template_file = open(template_path, "r")

    first_line = template_file.readline()

    if "# PARAMETERS:" in first_line:
        first_line = first_line.replace("# PARAMETERS:", "")
        return [param.strip() for param in first_line.split(",")]
    else:
        return []


def get_params_values(params):
    replacements = {}

    for param in params:
        key = "$$" + param.upper()
        replacements[key] = input(f"Value for '{param}': ")

    return replacements


def do_replacements_on(text, replacements):
    pattern = re.compile("|".join(re.escape(k) for k in replacements))

    return pattern.sub(lambda match: replacements[match.group(0)], text)


def process_template(template_path, output_path, replacements):
    print(f"Generating 'drone.yml' from '{template_path}'...")

    template_file = open(template_path, "r")
    output_file = open(output_path, "w")

    for line in template_file:
        if replacements:
            line = do_replacements_on(line, replacements)
        output_file.write(line)

    template_file.close()
    output_file.close()


def append_header_to_drone_yml(drone_path, text):
    drone_yml = open(drone_path, "r+")

    body = drone_yml.read()

    drone_yml.seek(0)

    drone_yml.write(text + body)

    drone_yml.close()


def dump_drone_yml(drone_path, template):
    print("Dumping content to 'drone.yml'")

    drone_yml = open(drone_path, "w")

    yaml.dump(template, drone_yml, default_flow_style=False)

    drone_yml.close()


def generate_drone_yml(args):
    print("Generating new 'drone.yml' from args...")

    template = {
        "kind": "pipeline",
        "name": "default",
        "clone": {
            "disable": True
        },
        "steps": []
    }

    if args["image"]:
        run_step = {
            "name": "run",
            "image": args["image"],
        }

        if args["run"]:
            run_step["commands"] = [args["run"]]

        template["steps"].append(run_step)

    if args["telegram"]:
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
