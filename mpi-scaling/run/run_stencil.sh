#!/bin/bash
# ----------------------------------------------------------------------
# File: run_stencil.sh
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Run a single MPI stencil test to measure baseline performance
# Usage:
#   cd mpi-scaling/run
#   ./run_stencil.sh
# Output:
#   ../performance/stencil_runtime_<NP>proc.txt
# Notes:
#   Adjust NP to change number of MPI processes
# ----------------------------------------------------------------------

# Number of MPI processes (adjust as needed)
NP=4

# Binary location
BINARY="../build/stencil_mpi"

# Output file for runtime
OUTPUT="../performance/stencil_runtime_${NP}proc.txt"

# Inform the user
echo "Running stencil_mpi with $NP MPI processes..."

# Run the program and save output
mpirun -np $NP $BINARY | tee $OUTPUT

echo "Runtime saved to $OUTPUT"
