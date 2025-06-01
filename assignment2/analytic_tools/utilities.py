"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
from pathlib import Path
import os
from typing import Dict, List


def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """

    # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    # Remember error handling
    try:
        dir = Path(dir)
    except:
        raise TypeError("Not a Path-like object")

    if not dir.exists():
        raise NotADirectoryError("Path to a non-existing directory")
    
    elif not dir.is_dir():
        raise NotADirectoryError("Not a real directory")

    # Traverse the directory and find its contents
    contents = list(dir.rglob("*"))

    # Count folders and total num. of files
    for path in contents:
        if path.is_file(): 
            res["files"] += 1
            if path.suffix == ".csv":
                res[".csv files"] += 1
            elif path.suffix == ".txt":
                res[".txt files"] += 1
            elif path.suffix == ".npy":
                res[".npy files"] += 1
            elif path.suffix == ".md":
                res[".md files"] += 1
            else:
                res["other files"] += 1
        elif path.is_dir(): 
            res["subdirectories"] += 1
    
    return res


def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """

    # Remember error handling
    try:
        dir = Path(dir)
    except:
        raise TypeError("Not a Path-like object")
    
    if not dir.exists():
        raise NotADirectoryError("Path to a non-existing directory")
    
    elif not dir.is_dir():
        raise NotADirectoryError("Not a real directory")
    
    if not isinstance(contents, Dict):
        raise TypeError("Not a dictionary")

    # Print the summary to the terminal
    print(f"\nDiagnostics for {dir}:")
    for item in contents.keys():
        print(f"Number of {item}: {contents[item]}")
    print("\n")


def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """
    # NOTE: This is a bonus task, if you implementing it, remove `raise NotImplementedError`
    raise NotImplementedError("Remove me if you implement this bonus task")

    ...


def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """

    # Do correct error handling first
    # Extract the filename from the .csv file and check if it is a valid greenhouse gas
    try:
        path = Path(path)
    except:
        raise TypeError("Not a Path-like object")
    
    if path.suffix != ".csv":
        raise ValueError("Not a '.csv' file")

    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]

    return path.stem in gasses # Bool


def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """

    # Do correct error handling first
    try:
        file_path = Path(file_path)
        dest_parent = Path(dest_parent)
    except:
        raise TypeError("Not a Path-like object")

    if not file_path.is_file():
        raise ValueError("Not a path to a file")
    
    if not is_gas_csv(file_path):
        raise ValueError("Not a '[gas].csv' file")
    
    if not dest_parent.is_dir():
        raise NotADirectoryError("Not an absolute directory or an existing directory")    

    # If the input file is valid:
    # Derive the name of the directory, pattern: gas_[gas_formula] directory
    dest_name = "gas_" + file_path.stem
    # Derive its absolute path
    dest_path = dest_parent/dest_name

    # Check if the directory already exists, and create one if not
    if dest_path.exists():
        return dest_path.absolute()
    else:
        dest_path.mkdir(parents=True,exist_ok=True)
        return dest_path.absolute()

def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """

    # Error handling first
    try:
        path = Path(path)
    except:
        raise TypeError("Not a Path-like object.")

    if os.path.sep not in str(path):
        raise ValueError("Path must have base name and parent name")

    # New, merged, basename of the path, which will be the new filename
    new_base = path.parent.name + "_" + path.name
    return new_base


def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    # NOTE: This is an optional task, no points assigned. If you are skipping it, remove `raise NotImplementedError` in the function body
    raise NotImplementedError("Remove me if you implement this optional task")

    ...
