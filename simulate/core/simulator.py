import numpy as np
import numpy.typing as npt
import os.path as osp
import pandas as pd

from . import Inputs, Optimiser


class Simulator:
    """Orchestrates the simulation
    """
    def __init__(
            self,
            inputs: Inputs,
            optimiser: Optimiser,
            output_path: str,
            solver: str = "CBC",
            is_debug: bool = False,
            model_format: str = "lp"
    ) -> None:
        """Constructor

        Parameters
        ----------
        inputs : Inputs
            inputs of the simulation
        optimiser : Optimiser
            optimiser object
        output_path : str
            folder to store the results of the simulation
        solver : str
            solver to perform the matrix multiplication
        is_debug : bool
            flag to run in debug mode
        model_format : str
            format of the model to be written (lp or mps)
        """
        self.inputs = inputs
        self._optimiser = optimiser
        self._output_path = output_path
        self._solver = solver
        self._is_debug = is_debug
        self._model_format = model_format

    def simulate(self) -> dict[str, npt.NDArray | float]:
        """Runs the simulation
        """
        results = self.__run_simulation()
        self.__save_results(results)

        return results

    def __run_simulation(self) -> dict[str, npt.NDArray | float]:
        """Runs the simulation
        """
        self._optimiser.initialise(
            inputs=self.inputs,
            output_path=self._output_path,
            solver=self._solver,
            is_debug=self._is_debug,
            model_format=self._model_format
        )
        self._optimiser.run()
        results = self.__read_results_from_model()

        return results

    def __read_results_from_model(self) -> dict[str, npt.NDArray | float]:
        """Reads the results from the pyomo model

        Returns
        -------
        results : dict[str, pd.Series]
            results of the optimisation
        """
        results = {}
        for variable in self.inputs.variables:
            results[variable] = pd.Series(getattr(self._optimiser._model, variable).get_values())
        results["objective_function"] = pd.Series(self._optimiser._model.objective_eqn.expr())

        return results

    def __save_results(self, results: dict[str, pd.Series]) -> None:
        """Saves the results in a csv
        """
        for key, val in results.items():
            val.to_csv(f"{osp.join(self._output_path, key)}.csv")
