# 463-Project-1

# Overview
# This project performs time-series clustering on short physiological signals (ABP segments) using:
- A divide and conquer recursive clustering strategy.
- A closest pair algorithm for validating cluster cohesion.
- Kadane’s algorithm for detecting high-activity intervals.

# this program will:
- Loads 10s ABP segments from a VitalDB `.mat` file
- Clusters segments via a simple divide-and-conquer split (no ML libs)
- Finds the closest pair in each cluster
- Runs Kadane’s algorithm on first-difference to find “active” intervals
- Shows quick matplotlib plots

# Quick start
1. Install Python 3.10+
2. Open the main script in VS Code and set:
DataPath = r"C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat" (you would need to input your own path for your data set)
3. Run the file, Plots will pop up.
4. Optional toy demo

# Installation
bash
pip install -r requirements.txt

Required packages: 
- numpy
- matplotlib
- h5py

The script prints:
- Cluster summary table
- Closest pair stats
- Kadane activity intervals
- 1–2 plots of closest pairs with shaded active regions

# Example Output:
<img width="1290" height="942" alt="image" src="https://github.com/user-attachments/assets/5b26b69a-b3f5-44d9-962a-0fd701c44aa9" />

<img width="448" height="316" alt="image" src="https://github.com/user-attachments/assets/911fdcfc-619c-4c88-bc97-57aedd33ce5d" />

<img width="1986" height="802" alt="image" src="https://github.com/user-attachments/assets/8b0d442f-f796-497a-8732-396b23fe5e8e" />

<img width="1998" height="778" alt="image" src="https://github.com/user-attachments/assets/e27480cd-03fd-4e30-98f6-d432d2d9336d" />



