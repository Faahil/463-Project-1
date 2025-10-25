# Time-Series Clustering and Segment Analysis on PulseDB Using Divide-and-Conquer Algorithms

**Author:** Faahil Ali  
**Course:** CMPSC 463 — Project 1

---

## Description of Project
This project develops a complete, algorithm-based pipeline to cluster and analyze biomedical time-series data from the **PulseDB** dataset.  

Instead of using machine learning, the system applies:
- **Divide-and-Conquer Clustering** – recursively splits time-series by similarity.
- **Closest Pair Algorithm** – validates cluster cohesion and selects representatives.
- **Kadane’s Algorithm** – finds the most active interval in each time series.

The system is tested on **1000 ABP (Arterial Blood Pressure)** segments (10-second windows).

---

## Installation and Usage
### Requirements
- Python 3.10+
- Packages: `numpy`, `matplotlib`, `h5py`

## Description of Project

This project focuses on clustering and analyzing biomedical time-series data from the PulseDB dataset using algorithmic methods rather than machine learning. The main goal is to group similar ten-second Arterial Blood Pressure (ABP) signal segments and analyze their internal structure using divide-and-conquer clustering, closest pair validation, and Kadane’s algorithm. The system loads the ABP data, recursively splits it into smaller clusters based on signal similarity, identifies the most similar pair within each cluster, and applies Kadane’s algorithm to find the most active interval in each signal. The overall idea is to demonstrate that clear, algorithmic reasoning alone can lead to meaningful segmentation and interpretation of biomedical data without using complex ML frameworks.

## Installation and Usage

The program runs in Python 3.10 or higher and requires three libraries: numpy, matplotlib, and h5py. After installing them with pip install -r requirements.txt, open the file named Ali – CMPSC 463 – Project 1.py and update the file path to your dataset. For example, set
DataPath = r"C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat".
After saving the file, run it in a terminal with python "Ali - CMPSC 463 – Project 1.py" (include quotes due to spaces and the dash). The console will print progress messages as it loads, clusters, and analyzes the data. It will also display information about the closest pairs and active signal intervals, followed by a few example plots that visualize the results. If you want to test the system without using the real dataset, you can set ShowToyCheck = True to run a small built-in toy example that verifies the functionality of each algorithm.

## Structure of Code

All code is written in a single Python file called Ali – CMPSC 463 – Project 1.py, which is organized into clearly separated sections. The program begins by loading and trimming the ABP signals from the .mat file through the function LoadAbpSegmentsFromMat. It then uses NormalizeSegments to standardize each time-series signal with z-score normalization so all signals can be compared fairly. The similarity between time-series segments is measured using either correlation distance or a simple Dynamic Time Warping (DTW) distance, depending on user preference. The main clustering process uses divide-and-conquer logic through the functions SplitCluster, RecursiveCluster, and RunClustering. These functions repeatedly split groups into smaller clusters based on similarity until they reach a defined size or depth limit. Inside each cluster, FindClosestPair checks for the most similar pair of signals to measure cluster cohesion. To analyze signal activity, the program uses Kadane’s algorithm through Kadane and GetActivePart, which detect the most active interval in each segment. Finally, ShowClusters generates visualizations that overlay the closest pairs and shade the active intervals found by Kadane’s algorithm. Supporting data classes such as Cluster, PairInfo, and KadaneOutput make the code cleaner and easier to follow.

## Description of Algorithms

The divide and conquer clustering algorithm starts with all signals in one large group and then recursively splits them into smaller ones. It selects two signals that are farthest apart and assigns each remaining signal to whichever of those two is more similar. This continues until each cluster becomes small enough or reaches the maximum recursion depth. The closest pair algorithm then compares all signals within each cluster to find the two most similar, providing a quick way to verify cluster consistency. Kadane’s algorithm is used to identify the most active part of each signal by analyzing the first difference and finding the interval with the largest cumulative change. Together, these algorithms create a logical and interpretable workflow that can identify patterns, similarities, and activity peaks in biomedical time-series data.

## Verification with Toy Example

The program includes a simple verification mode that generates small synthetic signals to confirm that each part of the algorithm works correctly. This toy test creates several short signals such as sine waves and spikes, then applies the full clustering process. The divide-and-conquer method successfully separates different waveform types, the closest pair function identifies which two signals are most similar, and Kadane’s algorithm highlights the most active portions. This helps confirm that the system performs correctly even without using the PulseDB dataset. It’s a good quick check before running the full experiment.

## Execution Results with 1000 Time Series

When running with the full PulseDB ABP dataset, the program loads up to 1000 segments, each about 625 samples long, and normalizes them. It then performs recursive clustering using correlation distance and creates around twenty or more clusters depending on the data distribution. The console prints information about the number of clusters, the size of each one, and the distances of the closest pairs. It also shows Kadane’s results for a few segments, including the start and end of their active ranges and the total activity value. Example output might include lines like:
“Loaded 1000 segments with 625 samples each,” followed by “Made 22 clusters. Example sizes: [45, 38, 62, 31, 52].”
The script also displays one or two plots showing the most similar pair within a cluster, along with shaded areas marking where Kadane’s algorithm detected peak activity.

## Discussion

The clustering results were consistent and matched expectations for physiological data. Signals with similar ABP waveforms tended to appear in the same clusters, and the closest pair distances were low, showing that the clustering logic worked effectively. Kadane’s algorithm correctly highlighted active intervals near the peaks and fast changes in the ABP signals, which helps explain why those signals were grouped together. The program’s performance was fast when using correlation distance and handled 1000 segments easily on a normal computer. Dynamic Time Warping worked as well but was slower, so it’s best for smaller runs. The main limitations are that the simple split strategy can create uneven cluster sizes and the stopping rule is based only on depth and size rather than an adaptive metric. Future improvements could include smarter seeding, better stopping conditions, and support for other signals such as ECG or PPG. Overall, the program met all the requirements and produced clear, interpretable results.

# Conclusions

In conclusion, this project successfully used divide-and-conquer clustering, closest pair analysis, and Kadane’s algorithm to explore and interpret biomedical time-series data from PulseDB. It proved that even without machine learning, basic algorithmic reasoning can effectively group and explain signal patterns in a meaningful way. The system is simple, efficient, and easy to understand, making it a strong demonstration of classical algorithms applied to real-world physiological data analysis.

## Block Diagram
flowchart TD
    A[Load .mat (ABP)] --> B[Normalize Data]
    B --> C{Divide & Conquer Split}
    C -->|Stop| D[Final Clusters]
    C -->|Split| C
    D --> E[Find Closest Pair]
    D --> F[Kadane's Algorithm on First Difference]
    E --> G[Cluster Stats Table]
    F --> H[Active Interval Highlights]
    G --> I[Console Summary]
    H --> J[Plots with Shaded Intervals]


