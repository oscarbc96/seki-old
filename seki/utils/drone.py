import subprocess


def run(command):
    command.insert(0, "drone")

    result = subprocess.run(command, stdout=subprocess.PIPE)

    return result.stdout.strip().decode("utf-8")
