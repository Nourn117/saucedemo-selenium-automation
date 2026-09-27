import os
import yaml

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.yaml")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as file:
        return yaml.safe_load(file)


CONFIG = load_config()
