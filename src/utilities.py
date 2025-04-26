import os
import subprocess
from datetime import date, datetime
from pathlib import Path

from src.logger import setup_logger

logging = setup_logger(__name__, verbose=True)


class Baker:

    def __init__(
        self,
        project_name: str,
        info: list,
        templates: list,
        structure: list,
        project_directory: Path,
    ):
        self.project_name = project_name
        self.project_directory = project_directory
        self.info = info
        self.templates = templates
        self.structure = structure
        self.formatted_date = self.get_formatted_date()
        self.year = datetime.now().year

    def get_formatted_date(self) -> str:
        """Format the current datetime as YYYY-mm-dd for use in CHANGELOG.md

        Returns:
            str: Formatted datetime
        """
        today = date.today()
        return today.strftime("%Y-%m-%d")

    def make_project_main_directory(self) -> None:
        """Make the main project directory"""
        logging.info(f"Creating project main directory: {self.project_directory}")
        os.makedirs(self.project_directory)

    def make_project_manifest(self, usr_subdirs: list) -> tuple:
        """Create a manifest of all subdirectories and files in project output directory

        Args:
            usr_subdirs (list): Additional user-provided list of subdirectories (from command line args)

        Returns:
            tuple: A list of files and subdirectories to create
        """
        logging.debug(f"Creating project structure from template...")
        subdirs = []
        init_files = []
        project_layout = self.structure["project_folder"]
        for item in project_layout:
            if type(item) == dict:
                files = item.values()
                dirs = item.keys()
                for dir in dirs:
                    subdirs.append(Path(f"{self.project_directory}/{str(dir)}"))
                for file in files:
                    for i in file:
                        file = Path(f"{self.project_directory}/{dir}/{i}")
                        init_files.append(file)
            else:
                dirpath = Path.joinpath(self.project_directory, item)
                init_files.append(dirpath)
        for usr_subdir in usr_subdirs:
            subdirs.append(Path.joinpath(self.project_directory, usr_subdir))
        logging.debug(f"Found the following dirs in structure: {subdirs}")
        logging.debug(f"Found the following init files: {init_files}")
        return subdirs, init_files

    def make_dirs_and_files(self, subdirs: list, init_files: list) -> None:
        """Write directories and files to disk in project output directory

        Args:
            subdirs (list): List of subdirectories for project directory to contain
            init_files (list): List of files to initialize within project directory/subdirectories
        """
        logging.info(f"Creating project files and folders...")
        for dir in subdirs:
            try:
                os.makedirs(dir, exist_ok=False)
                logging.debug(f"Created dir: {dir}")
            except FileExistsError as e:
                logging.warning(
                    f"Unable to make directory: {dir}.\nFile already exists: {e}"
                )
        for file in init_files:
            try:
                Path(file).touch()
                logging.debug(f"Created file: {file}")
            except FileExistsError as e:
                logging.warning(
                    f"Unable to create file: {file}\nFile already exists: {e}"
                )

    def _init_readme(self, filename: Path, template: str) -> None:
        """Write data to README.md

        Args:
            filename (Path): Name of output file
            template (str): Name of template to use
        """
        readme_header = f"# {self.project_name}\n\n"
        with open(filename, "a") as f:
            f.write(readme_header)
            f.write(template)

    def _init_license(self, filename: Path, template: str) -> None:
        """Write data to LICENSE

        Args:
            filename (Path): Name of output file
            template (str): Name of template to use
        """
        license_header = f"Copyright {self.year} {self.info['author']}\n\n"
        with open(filename, "a") as f:
            f.write(license_header)
            f.write(template)

    def _init_changelog(self, filename: Path, template: str) -> None:
        """Write data to CHANGELOG.md

        Args:
            filename (Path): Name of output file
            template (str): Name of template to use
        """
        changelog_header = (
            f"\n\n## [0.0.1] - {self.formatted_date}\n\n### Added\n\n- This file"
        )
        with open(filename, "a") as f:
            f.write(template)
            f.write(changelog_header)

    def write_init_file_data(self, init_files: list, init_file_templates: dict):
        """Write data to all initialized files in project directory

        Args:
            init_files (list): Files to write data to
            init_file_templates (dict): Templates to use for writing file data
        """
        logging.debug(f"Checking for init file templates....")
        templates = []
        for init_file in dict(init_file_templates).keys():
            init_file_template_name = str(init_file)
            templates.append(init_file_template_name)
        for file in init_files:
            filename = f"{Path(file).stem}{Path(file).suffix}"
            if filename in init_file_templates:
                template_data = dict(init_file_templates).pop(filename)
                init_filename = str(file)
                logging.debug(f"Found init template: {init_filename}")
                if filename == "CHANGELOG.md":
                    self._init_changelog(init_filename, template_data)
                elif filename == "README.md":
                    self._init_readme(init_filename, template_data)
                elif filename == "LICENSE":
                    self._init_license(init_filename, template_data)
                else:
                    with open(init_filename, "a") as f:
                        f.write(template_data)
            else:
                logging.debug(f"No template found for file: {filename}")

    def make_venv(self, venv: str) -> None:
        """Make a virtual environment in project output directory

        Args:
            venv (str): Name for virtual environment directory
        """
        subprocess.run(["python3", "-m", "venv", f"{venv}"], cwd=self.project_directory)

    def git_init(self) -> None:
        """Initialize a git repository in output project directory"""
        subprocess.run(["git", "init"], cwd=self.project_directory)
