import argparse
import os

from . import create_inputs
from .core import Optimiser, Simulator, Plotter


def main():
    print("Simulation of heating a building...")
    parser = argparse.ArgumentParser(description="Parsing the inputs to run the module.")
    parser.add_argument("-i", "--inputs", dest="inputs", help="TOML file with input data.")
    parser.add_argument("-o", "--output-path", dest="output_path", help="Path where to write the results.")
    parser.add_argument("-s", "--solver", dest="solver", help="Solver name (cbc, cplex ...)", default="cbc")
    parser.add_argument("-d", "--debug", dest="is_debug", action="store_true", help="Debug mode.")
    parser.add_argument("-m", "--model-format", dest="model_format", help="Output file formal (lp, mps ...")
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)

    inputs = create_inputs(args.inputs)
    simulator = Simulator(
        inputs=inputs,
        optimiser=Optimiser(),
        output_path=args.output_path,
        solver=args.solver,
        is_debug=args.is_debug,
        model_format=args.model_format
    )
    results = simulator.simulate()
    plotter = Plotter(
        inputs=inputs,
        simulation_results=results,
        output_path=args.output_path
    )
    plotter()

if __name__ == "__main__":
    main()
