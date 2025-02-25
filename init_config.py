import json
from json import JSONDecodeError


def initialise_config(path: str = "config.json") -> dict:
    try:
        with open(path, "r") as f:
            config = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"Config file not found {e}")
        return {}
    except JSONDecodeError as e:
        print(f"The json file is wrongly formatted {e}")
        return {}
    else:
        return config


config = initialise_config()