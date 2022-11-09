from dataclasses import dataclass, field
from typing import Any

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True, slots=True)
class Inputs:
    initial_temperature: int
    temperature_bounds: tuple[int, int]
    power_bounds: tuple[int, int]
    cooling_coefficient: int
    heating_coefficient: int
    cardinality_horizon: int
    step_size: int
    conversion_factor: int
    variables: list[str]
    horizon: npt.NDArray = field(init=False)
    temperature_ambient: npt.NDArray = field(init=False)
    cost_electricity: npt.NDArray = field(init=False)
    coefficient_heat_div_cool: int = field(init=False)

    def __post_init__(self) -> None:
        """Instantiates the remaining attributes (horizon, temperature_ambient, and cost_electricity)
        """
        time_set = np.arange(start=0, stop=self.cardinality_horizon, step=self.step_size)
        attrs = {
            "horizon": np.arange(start=0, stop=len(time_set), step=1),
            "temperature_ambient": 15 - np.sin(np.pi*(time_set+4)/12),
            "cost_electricity": 40 + 25*np.sin(np.pi*time_set/12)**2,
            "coefficient_heat_div_cool": self.heating_coefficient / self.cooling_coefficient
        }
        for key, val in attrs.items():
            self.__set_attribute(attribute=key, value=val)

    def __set_attribute(self, attribute: str, value: npt.NDArray | float) -> None:
        """Adds attribute to frozen object
        """
        object.__setattr__(self, attribute, value)