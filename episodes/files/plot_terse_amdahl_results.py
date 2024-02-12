import sys
import json
import matplotlib.pyplot as plt
import numpy as np

def process_files(file_list, output="plot.jpg"):
    value_tuples=[]
    for filename in file_list:
      # Open the JSON file and load data
      with open(filename, 'r') as file:
        data = json.load(file)
      value_tuples.append((data['nproc'], data['execution_time']))

    # Sort the tuples
    sorted_list = sorted(value_tuples)

    # Unzip the sorted list into two lists
    x, y = zip(*sorted_list)

    # Create a line plot
    plt.plot(x, y, marker='o')

    # Adding the y=1/x line
    x_line = np.linspace(1, max(x), 100)  # Create x values for the line
    y_line = (y[0]/x[0]) / x_line  # Calculate corresponding (scaled) y values

    plt.plot(x_line, y_line, linestyle='--', color='red', label='Perfect scaling')

    # Adding title and labels
    plt.title("Scaling plot")
    plt.xlabel("Number of cores")
    plt.ylabel("Wallclock time (seconds)")

    # Show the legend
    plt.legend()

    # Save the plot to a JPEG file
    plt.savefig(output, format='jpeg')

if __name__ == "__main__":
    # The first command-line argument is the script name itself, so we skip it
    output = sys.argv[1]
    filenames = sys.argv[2:]

    if filenames:
        process_files(filenames, output=output)
    else:
        print("No files provided.")

