import os
import json
from tai.constants import VERSION

home_dir = os.path.expanduser("~")
config_file_path = os.path.join(home_dir, ".tai")

class NoConfigException(Exception):
    pass

def write_config_file(secret_key):
    config = {"version": VERSION, "secret_key": secret_key}

    with open(config_file_path, "w") as outfile:
        json.dump(config, outfile)

def load_config_file():
    if not os.path.exists(config_file_path):
        raise NoConfigException(f"No config file found at {config_file_path}")
    with open(config_file_path, "r") as f:
        return json.load(f)
