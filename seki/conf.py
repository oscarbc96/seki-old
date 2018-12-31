import os
from pathlib import Path

home = Path.home()

REPOSITORY_PATH = os.path.join(home, ".seki")
DRONE_PATH = os.path.join(REPOSITORY_PATH, ".drone.yml")
