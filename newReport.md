# Time-Series Clustering and Segment Analysis on PulseDB Using Divide-and-Conquer Algorithms

**Author:** Faahil Ali  
**Course:** CMPSC 463 — Project 1

## Description of Project

This project clusters and analyzes short biomedical time-series segments from the PulseDB dataset using plain algorithms rather than machine learning. The focus is on ten second Arterial Blood Pressure segments. The pipeline loads the data, normalizes each segment, groups similar segments using a divide and conquer strategy, checks cluster cohesion by finding the most similar pair inside each cluster, and highlights the most active interval within each segment using Kadane’s algorithm on the first difference. The goal is to show that straightforward algorithmic reasoning can produce clear and explainable results on physiological signals without relying on heavy libraries.


## Data Type Considerations (ABP Signals)

This project focuses on **Arterial Blood Pressure (ABP)** signals from the PulseDB dataset. Each segment represents 10 seconds of continuous waveform data with approximately 625 samples. ABP signals are ideal for time-series clustering because they have periodic peaks corresponding to heartbeats and contain informative variations in amplitude and slope.

Before clustering, each segment is normalized using **z-score normalization** to ensure that similarity comparisons are based on waveform shape rather than absolute pressure values. This normalization step is essential for fair distance computation across subjects. Because biomedical signals may include small noise or baseline drifts, a light smoothing step may optionally be applied, but the focus remains on algorithmic clarity rather than preprocessing complexity.


## Installation and Usage

### Requirements
- Python 3.10+
- Packages: `numpy`, `matplotlib`, `h5py`
  
The code runs with Python version 3.10 or newer and needs `numpy`, `matplotlib`, and `h5py`. After installing these packages with pip install -r requirements.txt, open the file named `Ali – CMPSC 463 – Project 1.py` in your editor and set the `DataPath` variable to the location of your VitalDB mat file. For example you can set DataPath to 
```python 
C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat.
```
Save the file and run it from a terminal with python `Ali - CMPSC 463 – Project 1.py`. The program prints a short summary of clusters, closest pair distances, and Kadane intervals, and it opens one or two simple plots that overlay the closest pair in a cluster with the active windows shaded. If you want to verify the algorithms without a dataset, set `ShowToyCheck` to True and run the script to see a small synthetic demo.

## Structure of Code

Everything is in a single file called `Ali – CMPSC 463 – Project 1.py`. The data is loaded and trimmed by `LoadAbpSegmentsFromMat` which reads ABP from the Subset group inside the mat file and makes sure every segment has the same length. `NormalizeSegments` performs a z score per segment so that distance calculations are fair. The program measures similarity with correlation distance by default and also includes a simple DTW option for small tests. The divide and conquer clustering is implemented by `SplitCluster`, `RecursiveCluster`, and `RunClustering` which repeatedly split groups until they reach size or depth limits. Inside each final cluster the function `FindClosestPair` searches for the most similar pair which is used as a quick cohesion check and as a representative example. To find where a signal is most active the code runs Kadane on the first difference using Kadane and `GetActivePart`. `ShowClusters` produces quick matplotlib plots that overlay the closest pair and shade the active regions. Small `dataclasses` named `Cluster`, `PairInfo`, and `KadaneOutput` keep results tidy and readable.

### Class Summaries
`Cluster` stores the indices of the signals that belong to a final cluster.  
`PairInfo` holds the pair of indices inside a cluster that are most similar, plus their distance.  
`KadaneOutput` records the start index, end index, and sum for the maximum subarray on the first difference of a signal.

### Function and Class Summary

| **Name** | **Type** | **Purpose** |
|-----------|-----------|-------------|
| `LoadAbpSegmentsFromMat` | Function | Reads ABP segments from the `.mat` file and ensures consistent length. |
| `NormalizeSegments` | Function | Applies z-score normalization to each segment for fair distance comparison. |
| `SplitCluster`, `RecursiveCluster`, `RunClustering` | Functions | Implement the divide-and-conquer clustering process. |
| `FindClosestPair` | Function | Finds the most similar pair of signals within each cluster using correlation distance. |
| `Kadane` | Function | Runs Kadane’s algorithm on the first difference to find the most active subinterval. |
| `GetActivePart` | Function | Retrieves indices for the interval of maximum cumulative change. |
| `ShowClusters` | Function | Generates matplotlib plots for visualization of clusters and active intervals. |
| `Cluster` | Dataclass | Stores indices of signals belonging to a final cluster. |
| `PairInfo` | Dataclass | Records the closest pair indices and their distance. |
| `KadaneOutput` | Dataclass | Stores start, end, and sum for the maximum subarray segment. |


## Description of Algorithms

The divide and conquer clustering starts with all segments in one group. It chooses two seeds that are far apart and assigns every segment to the seed it is closer to. It then recurses on each side until the groups are small enough or a maximum recursion depth is reached. The closest pair search inside each cluster compares all pairs and keeps the minimum distance which serves as a simple cohesion measure and helps pick a representative pair. Kadane’s algorithm runs on the first difference of each segment and returns the contiguous interval with the largest cumulative change. This interval often aligns with physiologically meaningful events such as sharp upstrokes or strong peaks in ABP, which helps explain why certain segments belong together.

## Verification with Toy Example

The project includes a small toy mode that fabricates a few short signals such as sinusoids with slight phase shifts, a faster sinusoid, a scaled version, a flat signal, and a copy with a brief spike. Running the pipeline on this set shows that the divide and conquer split places similar shapes together, the closest pair is chosen sensibly, and Kadane highlights the expected high activity region on the spiky signal. This quick check confirms that the implementation behaves sensibly before using the real dataset.


## Sample Scenarios and Generalization

To show flexibility, the same pipeline was tested on short stock-like time series that simulate gradual trends and sudden jumps. The divide-and-conquer algorithm grouped similar trend patterns, and Kadane’s algorithm detected spikes as high-activity intervals. This demonstrates that the method generalizes beyond biomedical data, handling anomaly detection and trend analysis tasks with minimal adjustment.

## Execution Results with 1000 Time Series

When run on up to one thousand ABP segments (≈625 samples each), the program:

- Loads and normalizes all data

- Performs recursive clustering using correlation distance

- Forms roughly 20–25 clusters depending on the distribution

Example output:
``` python
Loaded 1000 segments with 625 samples each
Made 22 clusters
Cluster 1: meanDist=0.12  min=0.05  max=0.24
Cluster 2: meanDist=0.14  min=0.06  max=0.28
```


The program also displays several plots overlaying the closest pair per cluster and shading active intervals.

### Examples:

**Figure 1.** Example console output showing clustering results for 1000 ABP segments.

<img width="1290" height="942" alt="image" src="https://github.com/user-attachments/assets/5b26b69a-b3f5-44d9-962a-0fd701c44aa9" />

**Figure 2.** Overlay of two ABP signals from the same cluster with active intervals shaded.

<img width="448" height="316" alt="image" src="https://github.com/user-attachments/assets/911fdcfc-619c-4c88-bc97-57aedd33ce5d" />

**Figure 3.** Example of cluster visualization showing cohesion among waveform shapes.

<img width="1986" height="802" alt="image" src="https://github.com/user-attachments/assets/8b0d442f-f796-497a-8732-396b23fe5e8e" />

**Figure 4.** Example of waveform highlighting using Kadane’s algorithm on the first difference.

<img width="1998" height="778" alt="image" src="https://github.com/user-attachments/assets/e27480cd-03fd-4e30-98f6-d432d2d9336d" />

### Discussion of Results

The clusters align closely with waveform shapes. Segments with similar ABP patterns group together, and their lowest pairwise distances confirm strong cohesion. Kadane’s intervals usually capture systolic peaks, helping to explain cluster assignments. Correlation distance works efficiently for aligned signals; DTW offers flexibility for misaligned cases but is slower.

#### The main limitations are:

- The simple two-seed split may cause uneven cluster sizes in some cases.

- Stopping conditions are fixed rather than adaptive.

#### Future improvements:

- Add silhouette-based stopping criteria.

- Improve seed selection via k-means++ style initialization.

- Extend compatibility to ECG and PPG data for multimodal analysis.

## Conclusions

This project shows that a straightforward algorithmic pipeline can cluster and explain biomedical time-series data without any machine learning. Divide and conquer clustering groups similar segments, the closest pair search provides an easy cohesion check and a clear example to inspect, and Kadane highlights where each signal is most active. The system is simple, fast, and easy to understand which makes it a solid demonstration of classical algorithms applied to real physiological data.

## Block Diagram

Block diagram of the PulseDB time-series clustering pipeline:

```mermaid
flowchart TD
    A[Load .mat ABP] --> B[Normalize]
    B --> C{Divide and Conquer Split}
    C -->|Stop| D[Final Clusters]
    C -->|Split| C
    D --> E[Closest Pair Search]
    D --> F[Kadane on First Difference]
    E --> G[Cluster Cohesion Summary]
    F --> H[Active Interval Highlights]
    G --> I[Console Output]
    H --> J[Simple Plots]
