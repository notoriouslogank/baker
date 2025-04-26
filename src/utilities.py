import os
import subprocess
from datetime import date, datetime
from pathlib import Path

from src.logger import setup_logger

logging = setup_logger(__name__)
today = date.today()
year = datetime.now().year


class Baker:

    def __init__(self, project_directory, name, author):
        self.project_directory = project_directory
        self.project_name = name
        self.formatted_date = today.strftime("%Y-%m-%d")
        self.author = author

    def make_project_main_directory(self):
        logging.info(f"Creating project main directory: {self.project_directory}")
        os.makedirs(self.project_directory)

    def make_project_manifest(self, template: list, usr_subdirs: list):
        logging.debug(f"Creating project structure from template...")
        subdirs = []
        init_files = []
        for item in template:
            if type(item) == dict:
                dirs = item.keys()
                files = item.values()
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
        return (subdirs, init_files)

    def make_dirs_and_files(self, subdirs, init_files):
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

    def _init_readme(self, filename, template):
        readme_header = f"# {self.project_name}\n\n"
        with open(filename, "a") as f:
            f.write(readme_header)
            f.write(template)

    def _init_license(self, filename, template):
        license_header = f"Copyright {year} {self.author}\n\n"
        with open(filename, "a") as f:
            f.write(license_header)
            f.write(template)

    def _init_changelog(self, filename, template):
        changelog_header = (
            f"\n\n## [0.0.1] - {self.formatted_date}\n\n### Added\n\n- This file"
        )
        with open(filename, "a") as f:
            f.write(template)
            f.write(changelog_header)

    def write_init_file_data(self, init_files, init_file_templates):
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

    def make_venv(self, venv):
        subprocess.run(["python3", "-m", "venv", f"{venv}"], cwd=self.project_directory)

    def git_init(self):
        subprocess.run(["git", "init"], cwd=self.project_directory)
