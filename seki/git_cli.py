from git import Repo


def get_repository(folder):
    return Repo(folder)


def clone_repository(clone_url, folder):
    print("Clonning repo...")
    return Repo.clone_from(clone_url, folder)


def create_branch(repo, branch_name):
    print(f"Creating new branch '{branch_name}'...")
    repo.git.reset("--hard")

    repo.git.checkout("-b", branch_name)


def checkout_branch(repo, branch_name):
    repo.git.reset("--hard")

    repo.git.checkout(branch_name)


def commit(repo, message):
    repo.git.add("--all")

    repo.git.commit(m=message)

    short_sha = repo.head.object.hexsha[:7]

    print(f"Commit: '{short_sha}'")


def push_repository(repo, upstream=None):
    print("Pushing changes...")
    if upstream:
        repo.git.push("origin", upstream)
    else:
        repo.git.push()
