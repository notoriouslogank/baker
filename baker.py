import argparse
from pathlib import Path

from src import config, logger
from src.utilities import Baker

logging = logger.setup_logger(__name__, verbose=False)


def parse_args():
    logging.debug(f"Parsing args...")
    parser = argparse.ArgumentParser(
        description="Programmatically create a file structure for a fresh, blank Python project (inluding README, CHANGELOG, LICENSE, and src)"
    )
    parser.add_argument("name", help="Name for new project")
    parser.add_argument(
        "-d",
        "--destination",
        help="Directory to build new project in",
    )
    parser.add_argument(
        "-g",
        "--git",
        help="Initialize a git repository in the new project",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--subdirectories",
        help="Subdirectories to build inside main project directory",
        required=False,
        nargs="*",
    )
    parser.add_argument(
        "-t",
        "--template",
        help="Project template (basic or advanced)",
        default="advanced",
    )
    parser.add_argument(
        "--no-venv",
        help="Do not create a virtual environment in the project directory",
        action="store_true",
    )
    return parser.parse_args()


def make_project_path(destination: str | Path, name: str) -> Path:
    project_directory = Path.joinpath(destination, name)
    return project_directory


if __name__ == "__main__":
    logging.debug(f"Starting program...")
    args = parse_args()
    logging.debug(f"Parsed the following args: {args}")
    configs = config.load_config()
    logging.debug(f"Read the following configs: {configs}")

    default_directory = configs["default_directory"]
    usr_subdirs = []
    init_templates = []

    if args.template not in configs["template"]:
        logging.critical(f"Missing template: {args.template}!")
        logging.warning(f"Falling back to default template.")
        template = configs["template"]["basic"]["project_folder"]
    else:
        template = configs["template"][args.template]["project_folder"]

    if args.destination:
        project_directory = make_project_path(Path(args.destination), args.name)
    else:
        project_directory = make_project_path(Path(default_directory), args.name)

    if args.subdirectories:
        logging.debug(f"Got user subdirectories: {args.subdirectories}")
        for subdirectory in args.subdirectories:
            usr_subdirs.append(subdirectory)

    bake = Baker(project_directory, args.name, configs["author"])
    subdirs, init_files = bake.make_project_manifest(template, usr_subdirs)
    bake.make_project_main_directory()
    bake.make_dirs_and_files(subdirs, init_files)
    init_file_templates = configs["init_files"]
    bake.write_init_file_data(init_files, init_file_templates)

    if args.no_venv == True:
        logging.debug(f"[--no-venv] flag selected; not creating a virtual environment.")
    else:
        logging.debug(f"Creating virtual environment: {configs['venv']}")
        bake.make_venv(configs["venv"])

    if args.git == True:
        logging.debug(f"Initializing git repository...")
    else:
        logging.debug(f"Not initializing git repository. Exiting.")
