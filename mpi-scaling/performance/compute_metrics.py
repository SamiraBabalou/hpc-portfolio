"""
File: compute_metrics.py
Author: Samira Babalou
Date: 2026-01-15
Purpose:
    Compute speedup and parallel efficiency for MPI stencil scaling experiments.
    Reads all scaling_runtime_Xproc.txt files in performance folder.
Usage:
    python3 compute_metrics.py > metrics_results.txt
"""

import glob

# -----------------------------
# Step 1: Collect runtimes
# -----------------------------
runtimes = {}

# Find all scaling runtime files
for f in glob.glob("scaling_runtime_*proc.txt"):
    # Extract number of MPI processes from filename
    NP = int(f.split("_")[2].replace("proc.txt", ""))
    with open(f) as file:
        line = file.readline()
        runtime = float(line.split(":")[1].strip().split()[0])
        runtimes[NP] = runtime

# -----------------------------
# Step 2: Compute speedup and efficiency
# -----------------------------
# Baseline: smallest NP
T_baseline = runtimes[min(runtimes.keys())]

print(f"{'NP':>5} {'Runtime(s)':>12} {'Speedup':>10} {'Efficiency':>10}")
for NP in sorted(runtimes.keys()):
    runtime = runtimes[NP]
    speedup = T_baseline / runtime
    efficiency = speedup / NP
    print(f"{NP:>5} {runtime:>12.6f} {speedup:>10.3f} {efficiency:>10.3f}")
