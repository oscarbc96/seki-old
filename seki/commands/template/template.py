import re

import click


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
    click.echo(f"Generating 'drone.yml' from '{template_path}'...")

    template_file = open(template_path, "r")
    output_file = open(output_path, "w")

    for line in template_file:
        if replacements:
            line = do_replacements_on(line, replacements)
        output_file.write(line)

    template_file.close()
    output_file.close()
