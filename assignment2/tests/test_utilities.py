""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    
    # Convert to path
    example_config = Path(example_config)
    
    # Test dictionary
    test = {
        "files": 10,
        "subdirectories": 5,
        ".csv files": 8,
        ".txt files": 0,
        ".npy files": 2,
        ".md files": 0,
        "other files": 0,
    }

    res = get_diagnostics(example_config)

    # Assert that the test dict is correct
    assert res == test, "They don't have the same values"

@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        (NotADirectoryError, "Path_to_a_non-existing_directory"),   # Not an existing directory
        (NotADirectoryError, Path(__file__)), # Not a directory
        (TypeError, 1)  # Not Path-like
        # add more combinations of (exception, dir) here
    ],
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """
    
    # Check that exceptions are raised
    with pytest.raises(exception):
        get_diagnostics(dir)

@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """
    
    # Test 1: Check that the gas in the file stem isn't in the list of gases
    # Test 2: Check that the gas is listed
    # Test 3: Check that lowercase letters don't work
    # Test 4: Check that the file-name is a listed gas
    assert is_gas_csv("IN3110/IN3110-thisank/assignment2/C2O6.csv") == False, "It is a listed gas"
    assert is_gas_csv("CO2.csv") == True, "Not a listed gas"
    assert is_gas_csv("IN3110/n2o.csv") == False, "Lowercase letters work"
    assert is_gas_csv("IN3110/IN3110-thisank/assignment2/pollution_data/CH4.csv") == True, "Not a listed gas"


@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()), # Not a file
        (TypeError, False), # Not Path-like
        (ValueError, "not a file.py"),  # Not a .csv file
        (TypeError, 1)  # Not Path-like
        # add more combinations of (exception, path) here
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """
    
    # Check that exceptions are raised
    with pytest.raises(exception):
        is_gas_csv(path)


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
    
    # Src and dest directories (any)
    start = example_config/"pollution_data/by_src/src_"
    dest = example_config/"pollution_data_restructured/by_gas"
    
    # Gas by src as seen in figure 2
    src_gas = {
        "agriculture":"H2",
        "airtraffic":"CO2",
        "oil_and_gass":"CH4"
    }

    # Assert result for each key-value pair
    for src in src_gas.keys():
        if not dest.exists():
            dest.mkdir(parents=True,exist_ok=True) # Create pollution_data_restructured/by_gas subdirectory path
        assert get_dest_dir_from_csv_file(dest, str(start) + src + f"/{src_gas[src]}.csv") \
            == dest/f"gas_{src_gas[src]}", "Non-existing file or directory"


@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        (TypeError, False, 1), # Not Path-like
        (NotADirectoryError, "Not a directory", Path.cwd()/"pollution_data/by_src/src_agriculture/CH4.csv"),  # Not a [gas].csv file, run from assignment2
        (ValueError, Path(__file__).parent.absolute(), "not a file")    # Not a file
        # add more combinations of (exception, dest_parent, file_path) here
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """
    
    with pytest.raises(exception):
        get_dest_dir_from_csv_file(dest_parent, file_path)


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """
    
    # Check that the function works for this path and the parent path
    assert merge_parent_and_basename(Path(__file__)) == "tests_test_utilities.py", "Not a valid path"
    assert merge_parent_and_basename(Path(__file__).parent) == "assignment2_tests", "Not a valid path"


@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),    # Not Path-like
        (TypeError, False), # Not Path-like
        (ValueError, "in3110"), # Doesn't have a parent directory
        (ValueError, Path(__file__).drive)  # Doesn't have a parent directory
        # add more combinations of (exception, path) here
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        merge_parent_and_basename(path)
