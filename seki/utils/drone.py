from typing import Dict

import requests

from seki.conf import DRONE_SERVER, DRONE_TOKEN, SEKI_PROJECT_OWNER, SEKI_PROJECT_REPO


class Drone:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Drone, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {DRONE_TOKEN}"})

    def _do_get_request(self, path: str):
        response = self.session.get(f"{DRONE_SERVER}/{path}")
        response.raise_for_status()
        return response.json()

    def _do_post_request(self, path: str, data: Dict):
        response = self.session.post(f"{DRONE_SERVER}/{path}", json=data)
        response.raise_for_status()
        return response.json()

    def _do_delete_request(self, path: str):
        response = self.session.delete(f"{DRONE_SERVER}/{path}")
        response.raise_for_status()

    def is_enabled(self):
        return self._do_get_request(f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}")["active"]

    def enable_repository(self):
        self._do_post_request(f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}", {})

    def cron_list(self):
        return self._do_get_request(f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}/cron")

    def cron_create(self, name: str, expr: str, branch: str):
        return self._do_post_request(
            f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}/cron", {"name": name, "expr": expr, "branch": branch},
        )

    def cron_delete(self, name: str):
        self._do_delete_request(f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}/cron/{name}")

    def build_list(self):
        return self._do_get_request(f"api/repos/{SEKI_PROJECT_OWNER}/{SEKI_PROJECT_REPO}/builds")
