import sys
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def process_files(file_list, output="plot.jpg", overwrite=False):
    """
    Process a list of JSON files to extract and plot data.

    Parameters:
    - file_list: list of str, List of JSON filenames to process.
    - output: str, Filename for the output plot.
    - overwrite: bool, Flag to indicate if the output file should be overwritten if it exists.
    """
    # Check if the output file already exists
    if os.path.exists(output) and not overwrite:
        print(f"Error: Output file '{output}' already exists. Use --overwrite to overwrite it.")
        return

    value_tuples = []
    
    for filename in file_list:
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

    if not value_tuples:
        print("No valid data to plot.")
        return

    # Sort the tuples
    sorted_list = sorted(value_tuples)

    # Unzip the sorted list into two lists
    x, y = zip(*sorted_list)

    # Create a line plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', label='Measured data')

    # Adding the y=1/x line
    x_line = np.linspace(1, max(x), 100)  # Create x values for the line
    y_line = (y[0] / x[0]) / x_line  # Calculate corresponding (scaled) y values

    plt.plot(x_line, y_line, linestyle='--', color='red', label='Perfect scaling')

    # Adding title and labels
    plt.title("Scaling Plot")
    plt.xlabel("Number of Cores")
    plt.ylabel("Wallclock Time (seconds)")

    # Show the legend
    plt.legend()

    # Improve layout
    plt.tight_layout()

    # Save the plot to a JPEG file
    try:
        plt.savefig(output, format='jpeg')
        print(f"Plot saved as {output}.")
    except Exception as e:
        print(f"Error saving plot: {e}")

def print_help():
    """
    Print help message for the script usage.
    """
    help_message = """
    Usage: python script.py <output.jpg> <file1.json> <file2.json> ... [--overwrite] [--help]
    
    This script processes a list of JSON files containing 'nproc' and 'execution_time'
    data to generate a scaling plot and save it as a JPEG image.

    Parameters:
    - <output.jpg> : The filename for the output plot.
    - <file1.json> <file2.json> ... : List of JSON files to process.
    - --overwrite : Optional flag to overwrite the output file if it already exists.
    - --help : Display this help message.
    """
    print(help_message)

if __name__ == "__main__":
    if '--help' in sys.argv:
        print_help()
    elif len(sys.argv) < 3:
        print("Usage: python script.py <output.jpg> <file1.json> <file2.json> ... [--overwrite] [--help]")
    else:
        overwrite = False
        if '--overwrite' in sys.argv:
            overwrite = True
            sys.argv.remove('--overwrite')

        output = sys.argv[1]
        filenames = sys.argv[2:]

        if filenames:
            process_files(filenames, output=output, overwrite=overwrite)
        else:
            print("No files provided.")
