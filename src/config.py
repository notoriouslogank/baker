from pathlib import Path

import yaml

from src.logger import setup_logger

logging = setup_logger(__name__)

CONFIGFILE = "src/config.yaml"


def load_config():
    logging.debug(f"Reading from config file: {CONFIGFILE}")
    if not Path(CONFIGFILE).exists():
        logging.critical(f"No config file found!")
        raise FileNotFoundError(f"Config file not found: {CONFIGFILE}")
    with open(CONFIGFILE, "r") as f:
        return yaml.safe_load(f) or {}
