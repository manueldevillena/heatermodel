import toml

from simulate.core import Inputs


def read_input_file(input_file_path: str) -> dict:
    """Reads TOML file with inputs

    Parameters
    ----------
    input_file_path : str
        Path to the TOML inputs file

    Returns
    -------
    data : dict
        dictionary with the input data
    """
    with open(input_file_path) as inputs_file:
        data = toml.load(inputs_file)

    return data


def create_inputs(inputs_file: str) -> Inputs:
    """Creates the inputs object to be passed to the simulation

    Parameters
    ----------
    inputs_file : str
        path to TOML inputs file
    Returns
    -------
    inputs : Inputs
        inputs object
    """
    inputs = read_input_file(inputs_file)

    return Inputs(**inputs)
