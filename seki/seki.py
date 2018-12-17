import sys
from argparse import ArgumentParser
from datetime import datetime
from hashlib import md5
from os.path import exists as folder_exists

from seki.bitbucket import find_bitbucket_repository
from seki.drone_cli import (
    enable_drone_repository,
    add_drone_cron,
    drone_is_enabled
)
from seki.drone_template import (
    dump_drone_yml,
    generate_drone_yml,
    get_template_params,
    get_params_values,
    process_template,
    append_header_to_drone_yml
)
from seki.git_cli import (
    get_repository,
    clone_repository,
    create_branch,
    checkout_branch,
    commit,
    push_repository
)
from seki.utils import find_in_environ_or_ask

REPOSITORY_PATH = "/tmp/seki/run"
DRONE_PATH = REPOSITORY_PATH + "/.drone.yml"


def run(args):
    # Check if run project exists
    if not folder_exists(REPOSITORY_PATH):
        BITBUCKET_USER = find_in_environ_or_ask("BITBUCKET_USER")
        BITBUCKET_EMAIL = find_in_environ_or_ask("BITBUCKET_EMAIL")
        BITBUCKET_PASSWORD = find_in_environ_or_ask("BITBUCKET_PASSWORD")

        # Create Bitbucket repository if needed
        clone_url = find_bitbucket_repository(BITBUCKET_USER, BITBUCKET_PASSWORD, BITBUCKET_EMAIL)
        # Check if drone enable
        if not drone_is_enabled(f"{BITBUCKET_USER}/run"):
            # Enable drone
            enable_drone_repository(f"{BITBUCKET_USER}/run")
        # Clone project
        repo = clone_repository(clone_url, REPOSITORY_PATH)
    else:
        repo = get_repository(REPOSITORY_PATH)

        checkout_branch(repo, "master")

    cron = args.get("cron", False)

    if cron:
        branch_name = cron + " - " + args["args"]

        branch_name_hash = md5(branch_name.encode("utf-8")).hexdigest()

        create_branch(repo, branch_name_hash)

        checkout_branch(repo, branch_name_hash)

        add_drone_cron(f"{BITBUCKET_USER}/run", branch_name_hash, cron)
    else:
        branch_name_hash = None

    if args["template"]:
        params = get_template_params(args["template"])

        replacements = get_params_values(params)

        process_template(args["template"], DRONE_PATH, replacements)
    else:
        drone_yml = generate_drone_yml(args)

        dump_drone_yml(DRONE_PATH, drone_yml)

    header = "# " + args["args"] + "\n"

    append_header_to_drone_yml(DRONE_PATH, header)

    commit(repo, args["args"])

    push_repository(repo, upstream=branch_name_hash)


def main():
    parser = ArgumentParser()

    shared_parser = parser.add_argument_group("shared")

    shared_parser.add_argument("--cron",
                               choices=[
                                   "@hourly",
                                   "@daily",
                                   "@weekly",
                                   "@monthly",
                                   "@yearly"
                               ],
                               help="list of available crons")

    template_parser = parser.add_argument_group("template")

    template_parser.add_argument("--template", action="store", help="path to template")

    run_parser = parser.add_argument_group("custom run")

    run_parser.add_argument("--image", action="store", help="image to run")

    run_parser.add_argument("--run", action="store", help="arguments for the image")

    run_parser.add_argument("--telegram", action="store_true", help="notify build result on telegram")

    args = vars(parser.parse_args())

    current_time = datetime.now().isoformat(" ", "seconds")

    args["args"] = " ".join(sys.argv[1:]) + " - " + current_time

    run(args)


if __name__ == "__main__":
    main()
