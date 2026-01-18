"""
File: compute_metrics.py
Author: Samira Babalou
Date: 2026-01-15
Purpose:
    Compute speedup and parallel efficiency for
    MPI stencil scaling experiments.
    Reads all scaling_runtime_Xproc.txt files in
    performance folder.
Usage:
    python3 compute_metrics.py > metrics_results.txt
"""

import glob
import os

# -----------------------------
# Step 1: Locate this script's directory
# -----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Step 2: Collect runtimes
# -----------------------------
runtimes = {}

# Look for runtime files in the same directory as this script
pattern = os.path.join(SCRIPT_DIR, "scaling_runtime_*proc.txt")

for f in glob.glob(pattern):
    # Extract number of MPI processes from filename
    NP = int(os.path.basename(f).split("_")[2].replace("proc.txt", ""))
    with open(f) as file:
        line = file.readline()
        runtime = float(line.split(":")[1].strip().split()[0])
        runtimes[NP] = runtime

# -----------------------------
# Step 3: Safety check
# -----------------------------
if not runtimes:
    raise RuntimeError(
        "No scaling_runtime_*proc.txt files found. "
        "Did you run run_scaling.sh first?"
    )

# -----------------------------
# Step 4: Compute speedup and efficiency
# -----------------------------
T_baseline = runtimes[min(runtimes.keys())]

print(f"{'NP':>5} {'Runtime(s)':>12} {'Speedup':>10} {'Efficiency':>10}")

for NP in sorted(runtimes.keys()):
    runtime = runtimes[NP]
    speedup = T_baseline / runtime
    efficiency = speedup / NP
    print(
        f"{NP:>5} "
        f"{runtime:>12.6f} "
        f"{speedup:>10.3f} "
        f"{efficiency:>10.3f}"
    )
