# MPI Scaling Portfolio Project

## Quickstart
Run the project locally or in Docker with these steps:

### Using Docker (recommended)
```bash
# Build the Docker image (run from repo root)
docker build -t hpc-portfolio .

# Start an interactive container
docker run -it hpc-portfolio

# Inside the container, go to the run folder and execute scaling experiments
cd mpi-scaling/run
bash run_scaling.sh

# Generate plots
cd ../performance
python3 plot_metrics.py

# Generate PDF summary
cd ../reports
pandoc scaling_analysis.md -o scaling_summary.pdf


## Objective
Evaluate the **strong scaling behavior** of an MPI-based stencil computation by measuring runtime, speedup,
and parallel efficiency as the number of MPI processes increases.

---

## Methodology
- MPI program executes 100 iterations of a 1D stencil update.
- Wall-clock runtime is measured using `MPI_Wtime()`.
- `run_stencil.sh` performs a single representative MPI run.
- `run_scaling.sh` automates strong scaling experiments across multiple MPI process counts.
- Collected metrics include runtime, speedup, and parallel efficiency.
- All outputs are saved in `performance/` to ensure reproducibility.

---

## Key Findings
- Runtime decreases as the number of MPI processes increases, indicating effective strong scaling.
- Speedup is sublinear due to increasing communication overhead.
- Parallel efficiency declines with higher process counts, consistent with expected MPI behavior.
- Slurm job scripts demonstrate how the same experiments can be executed on an HPC cluster.

---

## Folder Structure
- `src/` : MPI source code
- `build/` : Compiled binaries
- `run/` : Experiment and job scripts  
  (`run_stencil.sh`, `run_scaling.sh`, `slurm_job.sh`)
- `performance/` : Runtime outputs and analysis scripts  
  (`compute_metrics.py`, `plot_metrics.py`)
- `reports/` : Analysis reports and visualizations  
  - `scaling_analysis.md` – detailed discussion of results  
  - `figures/` – runtime, speedup, and efficiency plots

---

## Performance Plots
The following plots are generated automatically from scaling experiments using `plot_metrics.py`
and stored in `reports/figures/`.

### Runtime vs Number of MPI Processes
![runtime_vs_np](reports/figures/runtime_vs_np.png)

### Speedup vs Number of MPI Processes
![speedup_vs_np](reports/figures/speedup_vs_np.png)

### Parallel Efficiency vs Number of MPI Processes
![efficiency_vs_np](reports/figures/efficiency_vs_np.png)

These figures illustrate the trade-offs between computation and communication as parallelism increases.

---

## Performance Analysis Report

The strong scaling results are summarized in a concise analysis report.

- 📄 **PDF summary:** `mpi-scaling/reports/scaling_summary.pdf`
- 📊 **Generated figures:** `mpi-scaling/reports/figures/`

The report includes:
- Runtime, speedup, and efficiency plots
- Interpretation of scaling behavior
- Fully reproducible methodology

To regenerate the report locally:
```bash
cd mpi-scaling/run
bash run_scaling.sh
cd ../performance
python3 plot_metrics.py
cd ../reports
pandoc scaling_analysis.md -o scaling_summary.pdf
