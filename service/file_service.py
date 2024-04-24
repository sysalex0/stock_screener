import os
from pathlib import Path


def create_directory_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
