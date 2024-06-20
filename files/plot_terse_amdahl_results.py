#!/usr/bin/env python3
import argparse
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('AGG')

description = """
Plot results of an Amdahl scaling study,
assuming the '--terse' output flag was used.
"""

def process_files(output, file_list):
    value_tuples=[]
    for filename in file_list:
      # Open the JSON file and load data
      try:
          with open(filename, 'r') as file:
              data = json.load(file)
          value_tuples.append((data['nproc'], data['execution_time']))
      except FileNotFoundError:
          print(f"Error: File {filename} not found.")
          return
      except json.JSONDecodeError:
          print(f"Error: File {filename} is not a valid JSON.")
          return
      except KeyError:
          print(f"Error: Missing required data in file {filename}.")
          return

    # Sort the tuples
    sorted_list = sorted(value_tuples)

    # Unzip the sorted list into two lists
    x, y = zip(*sorted_list)

    # Create a line plot
    plt.plot(x, y, marker='o')

    # Adding the y=1/x line
    x_line = np.linspace(1, max(x), 100)  # Create x values for the line
    y_line = (y[0] / x[0]) / x_line       # Calculate corresponding (scaled) y values

    plt.plot(x_line, y_line, linestyle='--',
             color='red', label='Perfect scaling')

    # Adding title and labels
    plt.title("Scaling plot")
    plt.xlabel("Number of cores")
    plt.ylabel("Wallclock time (seconds)")

    # Show the legend
    plt.legend()

    # Save the plot to the specified file
    plt.savefig(output, dpi=400, bbox_inches="tight")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=description,
        epilog="Brought to you by HPC Carpentry"
    )

    parser.add_argument(
        "--output",
        help="Image file to write (PNG or JPG)",
        required=True
    )

    parser.add_argument(
        "inputs",
        help="Amdahl terse output files (JSON)",
        nargs="+"
    )

    args = parser.parse_args()

    process_files(args.output, args.inputs)
