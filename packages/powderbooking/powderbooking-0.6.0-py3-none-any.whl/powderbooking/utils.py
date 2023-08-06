#  Copyright (c) 2021. Michael Kemna.

import os


def get_env_or_raise(env_name: str) -> str:
    value = os.environ.get(env_name)
    if value is None or value == "":
        raise EnvironmentError(
            f"An environmental variable was expected with the name {env_name}"
        )
    return value
