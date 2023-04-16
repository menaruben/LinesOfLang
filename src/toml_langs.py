import sys
from toml import load
from pathlib import Path

script_dir = Path( __file__ ).parent.absolute()
langs_toml = fr"{script_dir}/langs.toml"

def get_default_extensions() -> list:
    """
    returns the default extensions from the langs.toml file (must be in the same folder)
    """
    try:
        with open(langs_toml, encoding="utf-8") as file_path:
            data = load(file_path)

        default_extensions = []
        for lang in data:
            default_extensions.extend(data[lang]["extensions"])

        return default_extensions

    except FileNotFoundError as exception_message:
        print(f"Error loading langs.toml file: {exception_message}")
        sys.exit()

