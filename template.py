import logging
import os
from pathlib import Path


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s]: %(levelname)s - %(message)s:"
)


def create_directory(directory):
    """Creates a directory at the specified path."""
    try:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Create directory: {directory}")
    except OSError as e:
        logging.error(f"Error creating directory: {directory}\n{e}")


def create_empty_file(file_path):
    """Creates an empty file at the specified path."""
    try:
        with open(file_path, "w") as f:
            pass
        logging.info(f"Create empty file: {file_path}")
    except OSError as e:
        logging.error(f"Error creating file: {file_path}\n{e}")


def check_and_create_files(file_list):
    """Checks files in the list, creates directories and empty files if needed."""
    for file_path in file_list:
        try:
            path = Path(file_path)
            directory = path.parent

            if directory != "":
                create_directory(directory)

            if not path.exists() or path.stat().st_size == 0:
                create_empty_file(path)
            else:
                logging.info(f"{path.name} already exists")
        except Exception as e:
            logging.error(f"Error creating file: {file_path}\n{e}")


if __name__ == "__main__":
    project_name = "recommender_system"

    files_list = [
        ".github/workflows/.gitkeep",
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/logging/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/utils/utility.py",
        f"src/{project_name}/constants/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/pipeline/__init__.py",
        "config/config.yaml",
        "params/params.yaml",
        "main.py",
        "app.py",
        "Dockerfile",
        "requirements.txt",
        "setup.py",
        "notebooks/test.ipynb"
    ]

    check_and_create_files(files_list)
