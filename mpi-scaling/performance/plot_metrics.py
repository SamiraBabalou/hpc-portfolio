#!/usr/bin/env python3
# ----------------------------------------------------------------------
# File: plot_metrics.py
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Generate runtime, speedup, and efficiency plots from MPI scaling experiments
# Usage:
#   cd mpi-scaling/performance
#   python3 plot_metrics.py
# Output:
#   PNG plots saved in ../reports/figures/
# Notes:
#   - Requires matplotlib installed
#   - Reads files named scaling_runtime_<NP>proc.txt
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt  # library to create plots
import glob                       # to find all runtime files
import os                         # to handle file paths

# -------------------------------
# Set folder paths
# -------------------------------
performance_dir = "."                # current folder with runtime txt files
figures_dir = "../reports/figures"  # where plots will be saved

# Create figures folder if it doesn't exist
os.makedirs(figures_dir, exist_ok=True)

# Dictionary to store runtimes
runtimes = {}

# -------------------------------
# Read all scaling runtime files
# Files expected: scaling_runtime_2proc.txt, scaling_runtime_4proc.txt, etc.
# -------------------------------
for f in glob.glob(os.path.join(performance_dir, "scaling_runtime_*proc.txt")):
    # Extract number of processes (NP) from filename
    try:
        NP = int(f.split("_")[2].replace("proc.txt",""))
    except Exception as e:
        print(f"Warning: Could not extract NP from filename {f}: {e}")
        continue
    with open(f) as file:
        line = file.readline().strip()
        if not line:
            print(f"Warning: File {f} is empty")
            continue
        # Example line: Runtime: 0.002977 seconds
        parts = line.split(":")
        if len(parts) < 2:
            print(f"Warning: Unexpected format in {f}: {line}")
            continue
        try:
            runtime = float(parts[1].strip().split()[0])  # extract runtime value
        except Exception as e:
            print(f"Warning: Could not parse runtime in {f}: {e}")
            continue
        runtimes[NP] = runtime

# Sort process counts
NPs = sorted(runtimes.keys())
times = [runtimes[n] for n in NPs]

# -------------------------------
# Compute speedup and parallel efficiency
# Speedup = T2 / Tn, Efficiency = Speedup / N
# Baseline is 2 processes
# -------------------------------
if 2 not in runtimes:
    print("Error: Baseline runtime for 2 processes not found. Cannot compute speedup.")
    exit(1)
T2 = runtimes[2]
speedup = [T2 / t for t in times]
efficiency = [s / n for s, n in zip(speedup, NPs)]

# -------------------------------
# Plot runtime vs number of MPI processes
# -------------------------------
plt.figure()
plt.plot(NPs, times, 'o-', label='Runtime (s)')
plt.xlabel('Number of MPI Processes')
plt.ylabel('Runtime (s)')
plt.title('MPI Stencil Runtime Scaling')
plt.grid(True)
plt.savefig(os.path.join(figures_dir, 'runtime_vs_np.png'))

# -------------------------------
# Plot speedup vs number of MPI processes
# -------------------------------
plt.figure()
plt.plot(NPs, speedup, 'o-', label='Speedup')
plt.plot(NPs, NPs, 'k--', label='Ideal speedup')  # reference line for perfect scaling
plt.xlabel('Number of MPI Processes')
plt.ylabel('Speedup')
plt.title('MPI Stencil Speedup')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(figures_dir, 'speedup_vs_np.png'))

# -------------------------------
# Plot parallel efficiency vs number of MPI processes
# -------------------------------
plt.figure()
plt.plot(NPs, efficiency, 'o-', label='Efficiency')
plt.xlabel('Number of MPI Processes')
plt.ylabel('Parallel Efficiency')
plt.title('MPI Stencil Efficiency')
plt.grid(True)
plt.savefig(os.path.join(figures_dir, 'efficiency_vs_np.png'))

# -------------------------------
# Done
# -------------------------------
print(f"Plots saved in {figures_dir}")
