import os.path as osp
import pyomo.environ as pyo

from simulate.core import Inputs
from . import ObjectiveFunction, Constraints


class SolverError(Exception):
    """Custom error that is raised if the solver does not find an optimal solution
    """

    def __init__(self, message: str) -> None:
        """
        Parameters
        ----------
        message : str
            Message to be given to the error.
        """
        super().__init__(message)


class Optimiser:
    """Builds the mathematical program
    """
    def __init__(self) -> None:
        """Constructor
        """

        self._inputs: Inputs = None
        self._output_path: str = None
        self._solver: str = None
        self._is_debug: bool = None
        self._model_format: str = None
        self._model: pyo.Model = None

    def initialise(
            self,
            inputs: Inputs,
            output_path: str,
            solver: str = "CBC",
            is_debug: bool = False,
            model_format: str = "lp"
    ) -> None:
        """Initialises the optimiser

        Parameters
        ----------
        inputs : Inputs
            inputs of the simulation
        output_path : str
            folder to store the results of the simulation
        solver : str
            solver to perform the matrix multiplication
        is_debug : bool
            flag to run in debug mode
        model_format : str
            format of the model to be written (lp or mps)
        """
        self._inputs: Inputs = inputs
        self._output_path = output_path
        self._solver = solver
        self._is_debug = is_debug
        self._model_format = model_format

    def run(self) -> None:
        """Runs the optimisation
        """
        model = self._problem_build()
        self._problem_solve(model)

    def _problem_build(self) -> pyo.Model:
        """Builds the optimisation problem

        Returns
        -------
        model : pyo.Model
            pyomo model with sets, variables, and equations built
        """
        self._create_model()
        self._create_sets_variables_parameters()
        self._create_equations()
        if self._is_debug:
            self._create_lp_mps(self._output_path, self._model_format)

        return self._model

    def _create_model(self) -> None:
        """Creates a pyomo model
        """
        self._model = pyo.ConcreteModel()

    def _create_sets_variables_parameters(self) -> None:
        """Creates the sets variables and parameters within the pyomo model
        """
        # Sets
        self._model.horizon = pyo.Set(initialize=self._inputs.horizon)

        # Decision variables
        self._model.temperature_house = pyo.Var(
            self._model.horizon, within=pyo.Reals, bounds=self.__bounds_temperature_house
        )
        self._model.power_heater = pyo.Var(
            self._model.horizon, within=pyo.Reals, bounds=self.__bounds_power_heater
        )

    def _create_equations(self) -> None:
        """Creates (calls) the constraints and objective of the problem
        """
        ObjectiveFunction(self._model, self._inputs)()
        Constraints(self._model, self._inputs)()

    def _problem_solve(self, model: pyo.Model) -> None:
        """Solves the problem

        Parameters
        ----------
        model : pyo.Model
            pyomo model with sets, variables, and equations built
        """
        opt = pyo.SolverFactory(self._solver)
        results = opt.solve(model, tee=self._is_debug, keepfiles=False)
        self.__check_solve_status(results)

    def _create_lp_mps(self, output_path: str, model_format: str) -> None:
        """Creates lp file with the model for debugging purposes

        Parameters
        ----------
        output_path : str
            output path to write the lp file
        model_format : str
            model format (lp or mps)
        """
        self._model.write(osp.join(output_path, f"model.{model_format}"), io_options={'symbolic_solver_labels': True})

    @staticmethod
    def __check_solve_status(results) -> None:
        """Checks the solver status

        Parameters
        ----------
        results
            results of the optimisation
        """
        if (results.solver.status != pyo.SolverStatus.ok
                or results.solver.termination_condition not in {
                    pyo.TerminationCondition.optimal,
                    pyo.TerminationCondition.feasible
                }
        ):
            raise SolverError(
                f"Problem not properly solved.\n"
                f"Status: {results.solver.status}\n"
                f"termination condition: {results.solver.termination_condition})."
            )

    def __bounds_temperature_house(self, model: pyo.Model, time: pyo.Set) -> tuple[float, float]:
        """Defines the minimum and maximum values for the temperature in the house

        Parameters
        ----------
        model : pyo.Model
            pyomo model
        time : pyo.Set
            pyomo time set
        """
        return self._inputs.temperature_bounds[0], self._inputs.temperature_bounds[1]

    def __bounds_power_heater(self, model: pyo.Model, time: pyo.Set) -> tuple[float, float]:
        """Defines the minimum and maximum values for the power of the heater

        Parameters
        ----------
        model : pyo.Model
            pyomo model
        time : pyo.Set
            pyomo time set
        """
        return self._inputs.power_bounds[0], self._inputs.power_bounds[1]
