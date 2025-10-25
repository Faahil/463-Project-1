# Ali – CMPSC 463 – Project 1
## Time Series Clustering and Segment Analysis on PulseDB Using Divide and Conquer Algorithms

This project performs time series clustering and analysis on short Arterial Blood Pressure segments from the PulseDB dataset. It focuses on using classical algorithmic design instead of machine learning to group, compare, and interpret physiological data in a clear and explainable way.

The program reads PulseDB’s ten second ABP signals, normalizes them, and applies a divide and conquer method to form clusters based on similarity. Inside each cluster, it finds the most similar pair of signals to measure cohesion and uses Kadane’s algorithm to highlight the most active interval within each signal. Together, these steps create a complete and understandable pipeline that shows why certain signals belong together instead of grouping them blindly.

## How to Run the Project

Make sure you have Python 3.10 or newer installed on your computer. Then follow these steps:

1) Install the required libraries by running
```bash
pip install -r requirements.txt 
```
This installs numpy, matplotlib, and h5py.

2) Open the file named Ali – CMPSC 463 – Project 1.py in your code editor.

3) Change the line that sets DataPath so it points to your PulseDB file. For example:
```python
DataPath = r"C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat"
```

4) Save the file and run it in the terminal with
```
python "Ali - CMPSC 463 – Project 1.py"
```

5) The program will print progress updates, cluster information, closest pair results, and then show a few visual plots of the signals.

If you want to test the algorithms without using the PulseDB dataset, set
```python
ShowToyCheck = True
```

at the top of the script. When you run it again, it will generate a small example to verify that all algorithms are working correctly.

## What the Program Does

When the program runs, it loads up to 1000 ABP segments from the dataset and normalizes each signal so they can be compared fairly. It then performs recursive clustering using a divide and conquer strategy, finding the most similar pair of signals inside each cluster to measure how cohesive it is. Kadane’s algorithm runs on each signal to detect the most active time interval where the waveform changes the most.

The results are printed in the console and shown in a few simple plots that display the closest pairs and their highlighted active regions. The output includes a short summary of how many clusters were created, the distance between signals, and timing results for each step.

## Example Output:

Below are some sample figures that show the output. The shaded parts mark the active intervals found by Kadane’s algorithm while the overlapping lines represent the closest pair in a cluster.

<img width="1290" height="942" alt="image" src="https://github.com/user-attachments/assets/5b26b69a-b3f5-44d9-962a-0fd701c44aa9" />

<img width="448" height="316" alt="image" src="https://github.com/user-attachments/assets/911fdcfc-619c-4c88-bc97-57aedd33ce5d" />

<img width="1986" height="802" alt="image" src="https://github.com/user-attachments/assets/8b0d442f-f796-497a-8732-396b23fe5e8e" />

<img width="1998" height="778" alt="image" src="https://github.com/user-attachments/assets/e27480cd-03fd-4e30-98f6-d432d2d9336d" />

---

## Files Included

- Ali – CMPSC 463 – Project 1.py contains all logic and algorithms.
- Report.md is the written project report with full details and discussion.
- requirements.txt lists the libraries needed to run the program.
- README.md is this setup and overview guide.

## Credits
ABP data is from the open PulseDB dataset available through VitalDB and Kaggle.
