import csv
import numpy as np
import matplotlib.pyplot as plt

filepath = "vol_data.csv"
machVal = []

with open(filepath, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) >= 7:
            machVal.append(float(row[6]))

sol_filepath = "mach.sol"

nodes = len(machVal)

with open(sol_filepath, 'w') as solfile:
    # Header
    solfile.write("MeshVersionFormatted 1\n")
    solfile.write("Dimension 2\n")
    solfile.write("SolAtVertices\n")
    solfile.write(f"{nodes}\n")
    solfile.write("1 1\n\n")
    
    # Mach values
    for item in machVal:
        solfile.write(f"{item}\n")

    solfile.write("\nEND")
