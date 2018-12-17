from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import (
    Repository,
    RepositoryPayload,
    RepositoryForkPolicy
)
from requests.exceptions import HTTPError


def find_bitbucket_repository(user, password, email):
    bitbucket = Client(
        BasicAuthenticator(user, password, email)
    )

    try:
        print("Finding run project in bitbucket...")
        repository = Repository.find_repository_by_name_and_owner(
            repository_name="run",
            client=bitbucket
        )
    except HTTPError:
        print("Project not found")
        print("Creating project run...")

        repository = Repository.create(
            payload=RepositoryPayload({
                "name": "run",
                "is_private": True,
                "fork_policy": RepositoryForkPolicy.NO_FORKS,
            }),
            client=bitbucket
        )

    for link in repository.links["clone"]:
        if link["name"] == "https":
            return link["href"]
