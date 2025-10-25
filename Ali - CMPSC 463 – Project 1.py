# Ali - CMPSC 463 – Project 1

import os, math, random, time
from dataclasses import dataclass
from typing import List, Tuple, Callable, Dict
import h5py
import numpy as np
import matplotlib.pyplot as plt

# editable settings based on user needs
DataPath = r"C:\Users\faa32\Downloads\VitalDB_CalBased_Test_Subset.mat" #replace wit your pathfile for your data
MaxSegments = 1000
MaxClusterSize = 60
MinClusterSize = 15
MaxDepth = 10
SimilarityMetric = "corr"     # can also be "dtw"
DtwWindowFraction = 0.10
ShowToyCheck = False          # flip to True to run a tiny verification demo first


# functions
def NormalizeSegments(X: np.ndarray) -> np.ndarray:
    """Z-score normalize each time-series individually."""
    meanVals = X.mean(axis=1, keepdims=True)
    stdVals = X.std(axis=1, keepdims=True)
    stdVals[stdVals == 0] = 1.0  # prevent division by 0
    return (X - meanVals) / stdVals


def CorrDistance(a: np.ndarray, b: np.ndarray) -> float:
    """Correlation distance = 1 - Pearson correlation. Smaller means more similar."""
    if a.std() == 0 or b.std() == 0:
        return 0.0 if a.std() == b.std() == 0 else 1.0
    r = np.corrcoef(a, b)[0, 1]
    return 1.0 - float(r)

    # super basic DTW with a diagonal constraint window
def DtwDistance(a: np.ndarray, b: np.ndarray, window: int) -> float:

    L = len(a)
    window = max(window, abs(L - len(b)))
    bigNum = 1e15
    dtw = np.full((L + 1, L + 1), bigNum)
    dtw[0, 0] = 0.0
    for i in range(1, L + 1):
        jStart = max(1, i - window)
        jEnd = min(L, i + window)
        for j in range(jStart, jEnd + 1):
            cost = (a[i - 1] - b[j - 1]) ** 2
            dtw[i, j] = cost + min(dtw[i - 1, j], dtw[i, j - 1], dtw[i - 1, j - 1])
    return math.sqrt(dtw[L, L])

    # pick which distance function to use
def GetMetric(name: str, length: int):

    if name == "dtw":
        w = int(max(1, DtwWindowFraction * length))
        return lambda a, b: DtwDistance(a, b, w)
    return CorrDistance


# kadanes algorithm (finds peak activity) 
@dataclass
class KadaneOutput:
    Start: int
    End: int
    Sum: float

    # classic Kadanes algorithm to find the max sum subarray
def Kadane(arr: np.ndarray) -> KadaneOutput:

    bestSum, curSum = -1e18, 0.0
    start = bestStart = bestEnd = 0
    for i, x in enumerate(arr):
        if curSum <= 0:
            curSum = x
            start = i
        else:
            curSum += x
        if curSum > bestSum:
            bestSum, bestStart, bestEnd = curSum, start, i
    return KadaneOutput(bestStart, bestEnd, bestSum)

    # run kadane on the signals 1st diff to see where activity spikes
def GetActivePart(segment: np.ndarray) -> KadaneOutput:

    diff = np.diff(segment)
    return Kadane(diff)


# find the closest pair in a cluster
@dataclass
class PairInfo:
    I: int
    J: int
    Distance: float

   # brute force all pairs; return the closest ones
def FindClosestPair(X: np.ndarray, metric) -> PairInfo:
 
    n = X.shape[0]
    best = PairInfo(0, 1, metric(X[0], X[1]) if n >= 2 else float("inf"))
    for i in range(n):
        for j in range(i + 1, n):
            d = metric(X[i], X[j])
            if d < best.Distance:
                best = PairInfo(i, j, d)
    return best


# divide & conquer clustering 
@dataclass
class Cluster:
    Idx: List[int]

   # split a group in half based on which of 2 farthest points each item is closer to
def SplitCluster(X, idxs, metric):
 
    if len(idxs) <= 2:
        half = len(idxs) // 2
        return idxs[:half], idxs[half:]

    seed = random.choice(idxs)
    farA = max(idxs, key=lambda i: metric(X[seed], X[i]))
    farB = max(idxs, key=lambda i: metric(X[farA], X[i]))

    left, right = [], []
    for i in idxs:
        distA, distB = metric(X[farA], X[i]), metric(X[farB], X[i])
        (left if distA <= distB else right).append(i)

    if not left or not right:
        half = len(idxs) // 2
        return idxs[:half], idxs[half:]
    return left, right

    # recursively split groups until they’re small enough
def RecursiveCluster(X, idxs, metric, maxSize, minSize, depth, maxDepth, outList):

    n = len(idxs)
    if n <= minSize or depth >= maxDepth or n <= maxSize:
        outList.append(Cluster(idxs))
        return

    left, right = SplitCluster(X, idxs, metric)
    if len(left) == 0 or len(right) == 0 or len(left) == n or len(right) == n:
        outList.append(Cluster(idxs))
        return

    RecursiveCluster(X, left, metric, maxSize, minSize, depth + 1, maxDepth, outList)
    RecursiveCluster(X, right, metric, maxSize, minSize, depth + 1, maxDepth, outList)

    # set things up & run the recursive clustering
def RunClustering(X: np.ndarray, metricName: str) -> Tuple[List[Cluster], Callable]:

    metric = GetMetric(metricName, X.shape[1])
    idxs = list(range(X.shape[0]))
    clusters = []
    RecursiveCluster(X, idxs, metric, MaxClusterSize, MinClusterSize, 0, MaxDepth, clusters)
    return clusters, metric


# load data from the .mat file 
def LoadAbpSegmentsFromMat(path: str, limit: int = 1000) -> np.ndarray:
    #Pull ABP signals from the VitalDB .mat file.
    if not os.path.exists(path):
        raise FileNotFoundError(f"Can’t find this file: {path}")

    if os.path.isdir(path):
        raise IsADirectoryError(f"Path is a folder, not a .mat file: {path}")

    with h5py.File(path, "r") as f:
        subset = f["Subset"]
        signals = subset["Signals"]
        shape = signals.shape
        if len(shape) != 3:
            raise ValueError(f"Expected a 3D dataset, got {shape}")

        ch = 2 if shape[1] > 2 else shape[1] - 1
        abp = np.array(signals[:, ch, :])

        # keep same count as SBP/DBP labels if they exist
        if "SBP" in subset and "DBP" in subset:
            sbp = np.squeeze(subset["SBP"][:])
            dbp = np.squeeze(subset["DBP"][:])
            n = min(len(sbp), len(dbp), abp.shape[0])
            abp = abp[:n]

        N = min(limit, abp.shape[0])
        abp = abp[:N]
        targetLen = 625 if abp.shape[1] >= 625 else abp.shape[1]
        abp = abp[:, :targetLen].astype(float)
        if targetLen != 625:
            print(f"Note: using length {targetLen} samples (file shorter than 625).")
        return abp


# extra: quick cohesion stats (mean/min/max distances) for validation
def ClusterStats(Xc: np.ndarray, metric: Callable) -> Tuple[float, float, float]:
    # returns (mean_intra, min_pair, max_pair)
    n = Xc.shape[0]
    if n < 2:
        return (0.0, 0.0, 0.0)
    dsum, dcount = 0.0, 0
    dmin, dmax = float("inf"), 0.0
    for i in range(n):
        xi = Xc[i]
        for j in range(i + 1, n):
            d = metric(xi, Xc[j])
            dsum += d; dcount += 1
            if d < dmin: dmin = d
            if d > dmax: dmax = d
    return (dsum / dcount, dmin, dmax)


# plot results
def ShowClusters(X, clusters, closestPairs, kadaneMap, maxPlots=2):
    # display up to 2 clusters w/ their closest pair highlighted
    count = 0
    for cNum, cl in enumerate(clusters):
        if count >= maxPlots or len(cl.Idx) < 2:
            continue
        pair = closestPairs.get(cNum)
        if not pair:
            continue

        iGlobal, jGlobal = cl.Idx[pair.I], cl.Idx[pair.J]
        s1, s2 = X[iGlobal], X[jGlobal]
        k1, k2 = kadaneMap[iGlobal], kadaneMap[jGlobal]

        plt.figure(figsize=(10, 4))
        plt.title(f"Cluster {cNum}  |  Closest Pair Dist = {pair.Distance:.3f}")
        plt.plot(s1, label=f"Seg {iGlobal}")
        plt.plot(s2, label=f"Seg {jGlobal}")

        def Shade(ax, k, colorAlpha=0.2):
            ax.axvspan(k.Start, k.End + 1, alpha=colorAlpha)

        ax = plt.gca()
        Shade(ax, k1)
        Shade(ax, k2)

        plt.xlabel("Sample")
        plt.ylabel("Normalized ABP")
        plt.legend()
        plt.tight_layout()
        plt.show()
        count += 1


# optional: tiny toy verification for grader sanity
def RunToyVerification():
    print("\n[Toy Check] building a tiny fake dataset...")
    t = np.linspace(0, 2*np.pi, 120)
    s1 = np.sin(t)
    s2 = np.sin(t + 0.2)      # similar to s1
    s3 = np.sin(2*t)          # faster
    s4 = 0.5*np.sin(t) + 0.3  # scaled/offset
    s5 = np.zeros_like(t)     # flat
    s6 = s1.copy(); s6[40:60] += 1.0  # spike region

    Xtoy = np.vstack([s1, s2, s3, s4, s5, s6]).astype(float)
    Xtoy = NormalizeSegments(Xtoy)

    clusters, metric = RunClustering(Xtoy, "corr")
    print("[Toy Check] clusters:", [len(c.Idx) for c in clusters])

    toyPairs = {}
    for idx, cl in enumerate(clusters):
        if len(cl.Idx) >= 2:
            toyPairs[idx] = FindClosestPair(Xtoy[cl.Idx], metric)

    toyKadane = {i: GetActivePart(Xtoy[i]) for i in range(Xtoy.shape[0])}
    for i in range(Xtoy.shape[0]):
        k = toyKadane[i]
        print(f"[Toy] seg {i}: active [{k.Start}, {k.End}] sum={k.Sum:.3f}")

    ShowClusters(Xtoy, clusters, toyPairs, toyKadane, maxPlots=2)
    print("[Toy Check] done.\n")


# Main funcs of script
def main():
    # optional toy
    if ShowToyCheck:
        RunToyVerification()

    print("Reading ABP signals from:", DataPath)
    t0 = time.perf_counter()
    Xraw = LoadAbpSegmentsFromMat(DataPath, MaxSegments)
    t1 = time.perf_counter()
    print(f"Loaded {Xraw.shape[0]} segments with {Xraw.shape[1]} samples each.")

    Xnorm = NormalizeSegments(Xraw)
    t2 = time.perf_counter()

    print("\nStarting clustering using divide & conquer")
    clusters, metric = RunClustering(Xnorm, SimilarityMetric)
    t3 = time.perf_counter()
    print(f"Made {len(clusters)} clusters. Example sizes:", [len(c.Idx) for c in clusters[:5]])

    # Find closest pairs
    print("\nChecking for closest pairs inside clusters")
    closestPairs = {}
    for idx, cl in enumerate(clusters):
        if len(cl.Idx) >= 2:
            subset = Xnorm[cl.Idx]
            closestPairs[idx] = FindClosestPair(subset, metric)

    # print quick cohesion stats table for the first few clusters
    print("\nCluster summary (first 10):")
    print("Idx  Size  MeanDist  MinPair  MaxPair")
    for cIdx, cl in enumerate(clusters[:10]):
        Xc = Xnorm[cl.Idx]
        meanD, minD, maxD = ClusterStats(Xc, metric)
        print(f"{cIdx:>3}  {len(cl.Idx):>4}  {meanD:>8.3f}  {minD:>7.3f}  {maxD:>7.3f}")

    # Kadane analysis
    print("\nRunning Kadane on each segment to find active zones")
    tPairsStart = time.perf_counter()
    kadaneMap = {i: GetActivePart(Xnorm[i]) for i in range(Xnorm.shape[0])}
    t4 = time.perf_counter()
    for i in range(min(5, Xnorm.shape[0])):
        k = kadaneMap[i]
        print(f"Seg {i}: active range [{k.Start}, {k.End}]  sum={k.Sum:.3f}")

    print("\nDisplaying visualizations:")
    ShowClusters(Xnorm, clusters, closestPairs, kadaneMap, maxPlots=2)

    # timings (simple)
    print("\nTiming (seconds):")
    print(f"  load = {t1 - t0:.2f}")
    print(f"  normalize = {t2 - t1:.2f}")
    print(f"  cluster = {t3 - t2:.2f}")
    print(f"  pairs+kadane = {t4 - t3:.2f}")

    print("\nDone. Total clusters:", len(clusters))


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
