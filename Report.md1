# Ali – CMPSC 463 – Project 1  
**Title:** Time-Series Clustering and Segment Analysis on PulseDB Using Divide-and-Conquer Algorithms  

**Author:** Ali  
**Course:** CMPSC 463 — Project 1

---

## Description of Project
This project clusters and analyzes biomedical time-series data from the PulseDB dataset using straightforward algorithms instead of machine learning. The goal is to group similar ten-second Arterial Blood Pressure (ABP) segments and explain why they belong together. The system loads the ABP data, recursively splits it into smaller clusters based on signal similarity, identifies the most similar pair within each cluster to check cohesion, and applies Kadane’s algorithm on the first difference of each signal to find its most active interval. The result is an interpretable pipeline that demonstrates how basic algorithmic reasoning can segment and explain physiological signals.

---

## Installation and Usage
The program runs on Python 3.10 or newer and uses three libraries: `numpy`, `matplotlib`, and `h5py`. After installing them with `pip install -r requirements.txt`, 
open the file named **Ali – CMPSC 463 – Project 1.py** and set your data path, for example: DataPath = r"C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat"
Save the file and run: python "Ali - CMPSC 463 – Project 1.py"

The console prints clustering progress, the closest pair information, Kadane intervals, and timing. The script also pops up one or two simple Matplotlib plots. To verify the algorithms without a dataset, set `ShowToyCheck = True` to run a small synthetic test.

---

## Structure of Code
All logic lives in a single file, **Ali – CMPSC 463 – Project 1.py**. Data is loaded and trimmed with `LoadAbpSegmentsFromMat`, and each segment is normalized with `NormalizeSegments` so similarity comparisons are fair. The default similarity is correlation distance, with a simple DTW option provided for smaller tests. Clustering uses a divide-and-conquer routine via `SplitCluster`, `RecursiveCluster`, and `RunClustering`, which repeatedly split groups until they reach size or depth limits. Inside each cluster, `FindClosestPair` identifies the tightest pair to validate cohesion, while `Kadane` and `GetActivePart` find the most active interval of each signal. `ShowClusters` displays quick overlays of the closest pair with shaded active regions. Small data classes—`Cluster`, `PairInfo`, and `KadaneOutput`—keep results tidy and readable.

---

## Description of Algorithms
The divide-and-conquer clustering starts with all segments together, picks two far-apart seeds, and assigns each segment to whichever seed it is closer to. This split recurses until clusters are small enough or a maximum depth is reached. The closest pair search checks all pairs inside each cluster to find the minimum distance, which provides a simple measure of cohesion and a representative pair to inspect. Kadane’s algorithm runs on the first difference of each segment to highlight the interval with the largest cumulative change, which often lines up with meaningful physiological events.

---

## Verification with Toy Example
A built-in toy mode generates a handful of short synthetic signals such as sinusoids and a spiky signal. Running the full pipeline on these shows that similar waveforms cluster together, the closest pair function picks the expected pair, and Kadane highlights the high-activity window. This quick check confirms that the algorithms behave sensibly before running on the real dataset.

---

## Execution Results with 1000 Time Series
Using up to 1000 ABP segments of roughly 625 samples each, the program loads and normalizes the data, then creates around twenty or more clusters depending on the distribution. The console prints a short cluster summary table that includes mean, minimum, and maximum intra-cluster distances. It also prints a few example Kadane intervals and shows one or two plots with the closest pair overlaid and shaded active regions. Example output includes lines such as “Loaded 1000 segments with 625 samples each” and “Made 22 clusters. Example sizes: [45, 38, 62, 31, 52].” These results show the approach runs quickly with correlation distance and yields interpretable groups.

---

## Discussion
Overall, the clusters make sense: segments with similar ABP waveforms tend to end up together. The closest pair distances inside those clusters are low, which supports cluster cohesion. Kadane’s algorithm highlights intervals near strong upstrokes and peaks, which helps explain why certain segments belong in the same cluster. Performance is good for 1000 segments with correlation distance; DTW works but is slower and best for smaller subsets. The main limitations are the simple split rule, which can produce uneven groups, and a basic stopping rule that uses size and depth instead of an adaptive metric. Future work could add better seed selection, a silhouette-style stopping criterion, and support for additional signals like ECG or PPG.

---

## Conclusions
This project shows that a clean, algorithm-only pipeline—divide-and-conquer clustering, closest pair validation, and Kadane’s algorithm—can meaningfully cluster and interpret biomedical time-series data. The system is simple, efficient, and easy to follow, and it meets the project requirements while staying beginner-friendly.

---

## Block Diagram
```mermaid
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
