from base64 import b64decode, b64encode
from hashlib import md5 as base_md5


def string_to_b64(s: str) -> str:
    return str(b64encode(s.encode("utf-8")), "utf-8")


def b64_to_str(b: str) -> str:
    return b64decode(b).decode("utf-8")


def md5(s: str) -> str:
    return base_md5(s.encode("utf-8")).hexdigest()
