#!/bin/bash
# ----------------------------------------------------------------------
# File: run_scaling.sh
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Run strong scaling experiments for stencil_mpi
# Usage:
#   cd mpi-scaling/run
#   ./run_scaling.sh
# Output:
#   ../performance/scaling_runtime_<NP>proc.txt
# Notes:
#   Demonstrates how runtime changes as number of MPI processes increases
# ----------------------------------------------------------------------

BINARY="../build/stencil_mpi"
OUTPUT_DIR="../performance"

# Loop over multiple MPI process counts
for NP in 2 4 8
do
    echo "Running stencil_mpi with $NP MPI processes..."
    mpirun -np $NP $BINARY | tee $OUTPUT_DIR/scaling_runtime_${NP}proc.txt
done
