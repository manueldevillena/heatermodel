import numpy as np
import pyomo.environ as pyo


class Constraints:
    """Defines the constraints of the problem
    """
    def __init__(self, model, inputs) -> None:
        """Constructor
        """
        self._model = model
        self._inputs = inputs

    def __call__(self) -> None:
        self._model.temperature_house_eqn = pyo.Constraint(self._model.horizon, rule=self.__temperature_house)

    def __temperature_house(self, model: pyo.Model, t: pyo.Set) -> pyo.Constraint:
        """Computes the house temperature

        Parameters
        ----------
        model : pyo.Model
            pyomo model
        t : pyo.Set
            time-step

        Returns
        -------
        expr : expression of the house temperature
        """
        if t == 0:
            return model.temperature_house[t] == self._inputs.initial_temperature
        else:
            return model.temperature_house[t] == (
                    self._inputs.temperature_ambient[t] +
                    (self._inputs.coefficient_heat_div_cool * model.power_heater[t])
            )
