import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import os.path as osp

from . import Inputs


class Plotter:
    """Plots the results
    """
    def __init__(self, inputs: Inputs, simulation_results: dict[str, npt.NDArray | float], output_path: str) -> None:
        """Constructor

        Parameters
        ----------
        simulation_results : dict[str, npt.NDArray | float]
            dictionary with simulation results
        output_path : str
            path to directory to store results
        """
        self._inputs = inputs
        self._simulation_results = simulation_results
        self._output_path = output_path

    def __call__(self) -> None:
        """Calls all plots
        """
        self._plot_temp_power()
        self._plot_bounds()
        self._plot_price()
        self._plot_cost()

    def _plot_temp_power(self, name: str = "temp_power") -> None:
        """Line plot
        """
        time_horizon = np.arange(start=0, stop=self._inputs.cardinality_horizon, step=self._inputs.step_size)
        x_ticks = range(0, self._inputs.cardinality_horizon, 5)
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

        # Left axis
        colour = "tab:red"
        ax1.set_xlabel("Time Horizon [h]", fontsize=20)
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=0, fontsize=15)
        ax1.set_ylabel("Temperature [C]", color=colour, fontsize=20)
        ax1.tick_params(axis='y', labelcolor=colour)
        # ax1.set_ylim(12, 26)

        ax1.step(
            x=time_horizon, y=self._simulation_results["temperature_house"].values,
            alpha=0.8, color="r", linestyle="-", linewidth=2, label="Temperature house"
        )
        ax1.step(
            x=time_horizon, y=self._inputs.temperature_ambient,
            alpha=0.8, color="#ff4600", linestyle="-", linewidth=2, label="Temperature ambient"
        )
        # Right axis
        ax2 = ax1.twinx()
        colour = "tab:blue"
        ax2.set_ylabel("Power [kW]", color=colour, fontsize=20)
        ax2.tick_params(axis='y', labelcolor=colour)
        # ax2.set_ylim(2, 10)

        ax2.step(
            x=time_horizon, y=self._simulation_results["power_heater"].values,
            alpha=0.8, color="b", linestyle="-", linewidth=2, label="Power heater"
        )

        # Additional stuff
        plt.grid()
        ax1.legend(fontsize=18, loc=2)
        ax2.legend(fontsize=18, loc=1)
        plt.title("Optimal power and temperature")
        fig.tight_layout()
        fig.savefig(osp.join(self._output_path, f"{name}.pdf"))
        plt.close()

    def _plot_bounds(self, name: str = "bounds") -> None:
        """Line plot
        """
        time_horizon = np.arange(start=0, stop=self._inputs.cardinality_horizon, step=self._inputs.step_size)
        x_ticks = range(0, self._inputs.cardinality_horizon, 5)
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

        # Left axis
        colour = "tab:red"
        ax1.set_xlabel("Time Horizon [h]", fontsize=20)
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=0, fontsize=15)
        ax1.set_ylabel("Temperature [C]", color=colour, fontsize=20)
        ax1.tick_params(axis='y', labelcolor=colour)
        # ax1.set_ylim(20, 26)

        ax1.axhline(y=self._inputs.temperature_bounds[0], color="r", linestyle="--", alpha=0.7, label="Temperature bounds")
        ax1.axhline(y=self._inputs.temperature_bounds[1], color="r", linestyle="--", alpha=0.7)

        ax1.step(
            x=time_horizon, y=self._simulation_results["temperature_house"].values,
            alpha=0.8, color="r", linestyle="-", linewidth=2, label="Temperature house"
        )

        # Right axis
        ax2 = ax1.twinx()
        colour = "tab:blue"
        ax2.set_ylabel("Power [kWh]", color=colour, fontsize=20)
        ax2.tick_params(axis='y', labelcolor=colour)
        # ax2.set_ylim(3, 9)

        ax2.axhline(y=self._inputs.power_bounds[0], color="b", linestyle="--", alpha=0.7, label="Power bounds")
        ax2.axhline(y=self._inputs.power_bounds[1], color="b", linestyle="--", alpha=0.7)
        ax2.step(
            x=time_horizon, y=self._simulation_results["power_heater"].values,
            alpha=0.8, color="b", linestyle="-", linewidth=2, label="Power heater"
        )

        # Additional stuff
        plt.grid()
        ax1.legend(fontsize=18, loc=6)
        ax2.legend(fontsize=18, loc=5)
        fig.tight_layout()
        fig.savefig(osp.join(self._output_path, f"{name}.pdf"))
        plt.close()

    def _plot_price(self, name: str = "price") -> None:
        """Line plot
        """
        time_horizon = np.arange(start=0, stop=self._inputs.cardinality_horizon, step=self._inputs.step_size)
        x_ticks = range(0, self._inputs.cardinality_horizon, 5)

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

        # Left axis
        colour = "tab:orange"
        ax1.set_xlabel("Time Horizon [h]", fontsize=20)
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=0, fontsize=15)
        ax1.set_ylabel("Price [$/kWh]", color=colour, fontsize=20)
        ax1.tick_params(axis='y', labelcolor=colour)
        # ax1.set_ylim(20, 26)

        ax1.step(
            x=time_horizon, y=self._inputs.cost_electricity,
            alpha=0.8, color="#ff6d00", linestyle="-", linewidth=2, label="Price electricity"
        )

        # Right axis
        ax2 = ax1.twinx()
        colour = "tab:blue"
        ax2.set_ylabel("Power [kW]", color=colour, fontsize=20)
        ax2.tick_params(axis='y', labelcolor=colour)
        # ax2.set_ylim(3, 9)

        ax2.step(
            x=time_horizon, y=self._simulation_results["power_heater"].values,
            alpha=0.8, color="b", linestyle="-", linewidth=2, label="Power heater"
        )

        # Additional stuff
        plt.grid()
        ax1.legend(fontsize=18, loc=2)
        ax2.legend(fontsize=18, loc=1)
        plt.title(f"Total cost: ${self._simulation_results['objective_function'].values[0]:,.2f}")
        fig.tight_layout()
        fig.savefig(osp.join(self._output_path, f"{name}.pdf"))
        plt.close()

    def _plot_cost(self, name: str = "cost") -> None:
        """Line plot
        """
        time_horizon = np.arange(start=0, stop=self._inputs.cardinality_horizon, step=self._inputs.step_size)
        costs = self._inputs.cost_electricity * self._simulation_results["power_heater"].values * self._inputs.step_size
        x_ticks = range(0, self._inputs.cardinality_horizon, 5)

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

        # Left axis
        colour = "tab:red"
        ax1.set_xlabel("Time Horizon [h]", fontsize=20)
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=0, fontsize=15)
        ax1.set_ylabel("Cost [$]", color=colour, fontsize=20)
        ax1.tick_params(axis='y', labelcolor=colour)

        ax1.step(
            x=time_horizon, y=costs,
            alpha=0.8, color="r", linestyle="-", linewidth=2, label="Cost power"
        )

        # Additional stuff
        plt.grid()
        ax1.legend(fontsize=18, loc=2)
        plt.title(f"Total cost: ${self._simulation_results['objective_function'].values[0]:,.2f}")
        fig.tight_layout()
        fig.savefig(osp.join(self._output_path, f"{name}.pdf"))
        plt.close()
