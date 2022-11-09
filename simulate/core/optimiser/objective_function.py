import numpy as np
import pyomo.environ as pyo


class ObjectiveFunction:
    """Objective function(s) of the model
    """
    def __init__(self, model, inputs) -> None:
        """Constructor
        """
        self._model = model
        self._inputs = inputs

    def _objective_function(self, model: pyo.Model) -> pyo.Objective:
        """Minimises the costs of using the heater

        Parameters
        ----------
        model : pyo.Model
            pyomo model

        Returns
        -------
        expr : expression of the objective function
        """
        return pyo.quicksum(
            (
                self._inputs.cost_electricity[t] *
                model.power_heater[t] *
                self._inputs.step_size *
                self._inputs.conversion_factor
            )
            for t in model.horizon
        )

    def __call__(self) -> None:
        self._model.objective_eqn = pyo.Objective(rule=self._objective_function, sense=pyo.minimize)
