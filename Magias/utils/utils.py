"""Module with global utilities."""

import json


def get_global_vars_from_json(json_path: str) -> dict:
    """Returns a dictionary with the global variables from a json file."""
    with open(json_path, "r") as file:
        global_vars = json.load(file)

    return global_vars
