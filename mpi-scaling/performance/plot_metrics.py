#!/usr/bin/env python3
# ---------------------------------------------------------------
# File: plot_metrics.py
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Generate runtime, speedup, and efficiency plots from MPI
#          scaling experiments
# Usage:
#   python3 plot_metrics.py
# Output:
#   PNG plots saved in ../reports/figures/
# Notes:
#   - Requires matplotlib installed
#   - Reads files named scaling_runtime_<NP>proc.txt
# ---------------------------------------------------------------

import matplotlib.pyplot as plt
import glob
import os

# -------------------------------
# Set folder paths relative to this script
# -------------------------------
performance_dir = os.path.dirname(os.path.abspath(__file__))
figures_dir = os.path.join(performance_dir, "../reports/figures")
os.makedirs(figures_dir, exist_ok=True)

# -------------------------------
# Read all scaling runtime files
# -------------------------------
runtimes = {}
files = glob.glob(os.path.join(performance_dir, "scaling_runtime_*proc.txt"))
print(f"Found runtime files: {files}")  # Diagnostic for CI

for f in files:
    try:
        filename = os.path.basename(f)
        NP = int(filename.split("_")[2].replace("proc.txt", ""))
    except Exception as e:
        print(f"Warning: Could not extract NP from filename {f}: {e}")
        continue

    with open(f) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            try:
                # Accept "key: value" or just a number
                if ":" in line:
                    runtime = float(line.split(":")[1].strip().split()[0])
                else:
                    runtime = float(line.split()[0])
                runtimes[NP] = runtime
                break  # first valid line only
            except Exception as e:
                print(f"Warning: Could not parse runtime in {f}: {e}")
                continue

if not runtimes:
    print("Error: No valid runtime files found. Cannot compute speedup.")
    exit(1)

# -------------------------------
# Compute speedup and parallel efficiency
# -------------------------------
NPs = sorted(runtimes.keys())
times = [runtimes[n] for n in NPs]

if 2 not in runtimes:
    print("Error: Baseline runtime for 2 processes not found. " \
    "Cannot compute speedup.")
    exit(1)

T2 = runtimes[2]
speedup = [T2 / t for t in times]
efficiency = [s / n for s, n in zip(speedup, NPs)]

# -------------------------------
# Plot runtime
# -------------------------------
plt.figure()
plt.plot(NPs, times, "o-", label="Runtime (s)")
plt.xlabel("Number of MPI Processes")
plt.ylabel("Runtime (s)")
plt.title("MPI Stencil Runtime Scaling")
plt.grid(True)
plt.savefig(os.path.join(figures_dir, "runtime_vs_np.png"))

# -------------------------------
# Plot speedup
# -------------------------------
plt.figure()
plt.plot(NPs, speedup, "o-", label="Speedup")
plt.plot(NPs, NPs, "k--", label="Ideal speedup")
plt.xlabel("Number of MPI Processes")
plt.ylabel("Speedup")
plt.title("MPI Stencil Speedup")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(figures_dir, "speedup_vs_np.png"))

# -------------------------------
# Plot efficiency
# -------------------------------
plt.figure()
plt.plot(NPs, efficiency, "o-", label="Efficiency")
plt.xlabel("Number of MPI Processes")
plt.ylabel("Parallel Efficiency")
plt.title("MPI Stencil Efficiency")
plt.grid(True)
plt.savefig(os.path.join(figures_dir, "efficiency_vs_np.png"))

# -------------------------------
# Done
# -------------------------------
print(f"Plots saved in {figures_dir}")
