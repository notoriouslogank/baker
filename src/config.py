from pathlib import Path

import yaml

from src.logger import setup_logger

logging = setup_logger(__name__)

CONFIGFILE = "src/config.yaml"
INFOFILE = "config/info.yaml"
STRUCTURES = "config/structures.yaml"
TEMPLATES = "config/templates.yaml"


def load_templates() -> dict:
    """Parse the templates.yaml file and return relevant template

    Raises:
        FileNotFoundError: Unable to locate templates.yaml

    Returns:
        dict: Templates for various init files
    """
    logging.debug(f"Reading from config file: {TEMPLATES}")
    if not Path(TEMPLATES).exists():
        logging.critical(f"No templates file found!")
        raise FileNotFoundError(f"Config file missing: {TEMPLATES}")
    with open(TEMPLATES, "r") as f:
        return yaml.safe_load(f) or {}


def load_structures() -> dict:
    """Parse structures.yaml and return relevant file structure

    Raises:
        FileNotFoundError: Unable to locate structures.yaml

    Returns:
        dict: File and folder structure of project directory
    """
    logging.debug(f"Reading from config file: {STRUCTURES}")
    if not Path(STRUCTURES).exists():
        logging.critical(f"No structures file found!")
        raise FileNotFoundError(f"Config file missing: {STRUCTURES}")
    with open(STRUCTURES, "r") as f:
        return yaml.safe_load(f) or {}


def load_info() -> dict:
    """Parse info.yaml and return relevant information

    Raises:
        FileNotFoundError: Unable to locate info.yaml

    Returns:
        dict: Information about output path, venv, author
    """
    logging.debug(f"Reading from config file: {INFOFILE}")
    if not Path(INFOFILE).exists():
        logging.critical(f"No info file found!")
        raise FileNotFoundError(f"Config file missing: {INFOFILE}")
    with open(INFOFILE, "r") as f:
        return yaml.safe_load(f) or {}


def load_configs() -> tuple:
    """Load and return all configs

    Returns:
        tuple: Config data from info.yaml, templates.yaml, and structures.yaml
    """
    info = load_info()
    templates = load_templates()
    structures = load_structures()
    return info, templates, structures
