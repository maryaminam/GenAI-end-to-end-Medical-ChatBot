#resuable code to create a directory structure and empty files if they do not exist for another project

import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] : %(message)s:')


list_of_files = [
    "src/__init__.py",
    "src/helpers.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trails.ipynb"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    filedir, filename = os.path.split(file_path)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file: {filename}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):  
        with open(file_path, 'w') as f:
            pass
            logging.info(f"Creating empty file: {file_path}")
    else:
        logging.info(f"File already exists: {file_path}")