#!/bin/bash
# ----------------------------------------------------------------------
# File: slurm_job.sh
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Run stencil MPI strong scaling experiments on HPC cluster
# Usage:
#   sbatch slurm_job.sh
# Output:
#   ../performance/slurm_runtime_<jobid>.txt
# Notes:
#   Demonstrates multi-node, multi-task MPI execution with SLURM
#   Includes loop over multiple process counts for strong scaling
# ----------------------------------------------------------------------

#SBATCH --job-name=stencil_mpi
#SBATCH --output=../performance/slurm_runtime_%j.txt
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --mem=2G
#SBATCH --time=00:15:00
#SBATCH --partition=debug
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=your_email@example.com

# Load MPI module
module load openmpi

# -------------------------------
# Strong scaling experiment loop
# -------------------------------
for NP in 2 4 8 16
do
    echo "Running stencil_mpi with $NP MPI processes on SLURM..."
    srun -n $NP ../build/stencil_mpi
done

# -------------------------------
# HPC Notes:
# - Submit job: sbatch slurm_job.sh
# - Check queue: squeue -u $USER
# - Cancel job: scancel <job_id>
# -------------------------------
