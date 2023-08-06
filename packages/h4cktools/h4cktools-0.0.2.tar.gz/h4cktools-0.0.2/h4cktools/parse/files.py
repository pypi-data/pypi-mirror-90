import json
from pathlib import Path
import zipfile
import tarfile


__all__ = ["loadlist"]


def loadlist(
    file_path: str, 
    separator: str = "", 
    strip: bool = True,
    replace: dict = {},
    ignores: list = []
) -> list:
    """Loads list from a text file
    
    Args:
        file_path: path to list file
    
    Keywords:
        separator (str): separator use to split lines
        replace (dict): dict containing strings to replace
        ignore (list): ignore each lines that starts with an element

    Returns:
        list: list of loaded words
    """
    loaded_list = []
    with open(file_path, "r", errors="ignore") as file:
        for line in file:
            to_ign = False
            for ignore in ignores:
                if line.startswith(ignore):
                    to_ign = True
                    break
            if to_ign:
                continue

            if strip:
                line = line.strip()
            for key, value in replace.items():
                line = line.replace(key, value)
            loaded_list.append(line)
    return loaded_list