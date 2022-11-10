## Description

This model is an optimisation framework to calculate the optimal schedule of a heater to maintain the temperature of a building withincertain boundsa.

This model is cast as a Linear Program (LP) using formal optimisation techniques.

## Quick start

This program is written in Python 3.10.6, and requires a commercial solver (e.g., CBC, gurobi, or CPLEX).

### Install Python

This quick start guide does not go through the Python installation. However, I recommend the use of `pyenv` for this. Check the github page on this [link](https://github.com/pyenv/pyenv).

### Install Python environment
The Python environment is based on Poetry, although pip can also be used to make it work (not tested).

#### Install through poetry (recommended)

If you have poetry installed in your machine, you can simply run `poetry install` from the root directory of ther erpository. This will create and install an Python environment from the `poetry.lock` file using your default poetry settings. Note that if you do not have poetry configure to create the Python environments on your working directory, they will be created in a default location, to change this setting in poetry, run `poetry config virtualenvs.in-project true` before creating the environment.

#### Install through pip

Alternatively, a `requirements.txt` is generated regularly from the `poetry.lock` file. The `requirements.txt` can be used in a traditional fashion to install the Python environment via `pip install`. However, note that these requirements may not be up to date at all times and you can generate them yourself by running `poetry export --format requirements.txt --with dev --output requirements.txt`. Once the requirements are there, you can install them using `pip` in a virtual environment which you can create with `venv`:

```bash
python -m venv <MY_ENV>
source <MY_ENV>/bin/activate
(<MY_ENV>) pip install --upgrade pip
(<MY_ENV>) pip install -r requirements.txt
```

### Install solver

Most commercial solvers deal with LPs. CBC is the recommended solver as it is open source, although gurobi has been tested as well. To install CBC:

- ArchLinux (and Manjaro): `sudo pacman -S coin-or-cbc`

- MacOS: `brew tap coin-or-tools/coinor && brew install cbc`

- Ubuntu: `sudo apt install coinor-cbc`

### Run the code

To run the program you can use the provided `driver.sh`, and modify it to your specifications. Alternatively, you can run the helper:

```bash
python -m simulate -h
```

The simulation requires four options:

- -i --inputs: path to the TOML file with input data

- -o --output-path: path to the folder where you want to store the results

- -s --solver: solver that you want to use (e.g., cbc)

- -d: run in debug mode (writes the lp files of the optimisation for further inspection).

- -m: model format to with the file (lp or mps)


The input data is encoded in a TOML file. This file contains:

- initial_temperature (float): Initial temperature in Celsius

- temperature_bounds (list): Temperature bounds in Celsius

- power_bounds (list): Power of the heater in kW

- cooling_coefficient (float): Cooling coeficient in 1/h

- heating_coefficient (float): Heating coefficient in Celsius/kWh

- cardinality_horizon (int): Cardinality of the horizon in hours

- step_size (float): Step size of the horizon (resolution) in hours

- conversion_factor (float): Conversion from kW to MW

- variables (list(str)): variables to extract at the end of the optimisation # ["temperature_house", "power_heater"]

To run the code, these parameters must be encapsulated in a single TOML file that will be called when running. An example can be run typing the following command:
```bash
python -m simulate -i instances/example.toml -o results/example -s cbc -d -m lp
```
The same example can be found in the provided `driver.sh`.

## Formulation

The problem formulation is included in this repository in a file called `heater_model_documentation.pdf`.

## Q&A

For any questions regarding this model, contact Miguel Manuel de Villena at m.manueldevillena@gmail.com.


