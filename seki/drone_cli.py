import subprocess
from sys import exit


def run_drone_command(command):
    command.insert(0, "drone")

    result = subprocess.run(command, stdout=subprocess.PIPE)

    return result.stdout.strip().decode("utf-8")


def drone_is_enabled(repository):
    result = run_drone_command([
        "repo",
        "info",
        repository,
        "--format",
        "{{.Active}}"
    ])

    return "true" in result


def enable_drone_repository(repository):
    print("Enabling drone...")
    # Drone sync
    result = run_drone_command([
        "repo",
        "sync"
    ])

    if repository not in result:
        print("Drone sync failed")
        exit()

    # Enable project
    result = run_drone_command([
        "repo",
        "enable",
        repository
    ])

    if "Successfully activated repository" not in result:
        print("Not able to activate repository in drone")
        exit()


def add_drone_cron(repository, branch, cron_expr):
    run_drone_command([
        "cron",
        "add",
        "--branch",
        branch,
        repository,
        branch,  # name for cron
        cron_expr
    ])
