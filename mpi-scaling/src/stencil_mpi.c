/*
 * File: stencil_mpi.c
 * Author: Samira Babalou
 * Date: 2026-01-15
 * Description:
 *   MPI program to perform a 1D stencil computation.
 *   Demonstrates point-to-point communication, MPI_Sendrecv, and strong scaling.
 * Purpose:
 *   Portfolio-ready HPC code to showcase parallelization skills.
 * Compilation:
 *   mpicc stencil_mpi.c -O3 -o stencil_mpi
 * Execution:
 *   mpirun -np <num_processes> ./stencil_mpi
 */

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {

    // Initialize MPI environment
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // process ID
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // total number of processes

    const int N = 2000;                  // total array size
    int local_n = N / size;              // portion of array per process

    // Allocate local arrays
    double *data = (double*)malloc(local_n * sizeof(double));
    double *recv = (double*)malloc(local_n * sizeof(double));

    // Initialize data array (for demonstration, each rank fills its value)
    for (int i = 0; i < local_n; i++)
        data[i] = rank * 1.0;

    // Start timer for performance measurement
    double start = MPI_Wtime();

    // 100-step 1D stencil computation
    for (int step = 0; step < 100; step++) {
        int left = (rank - 1 + size) % size;
        int right = (rank + 1) % size;

        // Exchange data with neighbors
        MPI_Sendrecv(
            data, local_n, MPI_DOUBLE, right, 0,
            recv, local_n, MPI_DOUBLE, left, 0,
            MPI_COMM_WORLD, MPI_STATUS_IGNORE
        );

        // Simple stencil update
        for (int i = 0; i < local_n; i++)
            data[i] = 0.5 * (data[i] + recv[i]);
    }

    // Stop timer
    double end = MPI_Wtime();

    // Only rank 0 prints runtime
    if (rank == 0)
        printf("Runtime: %f seconds\n", end - start);

    // Free memory
    free(data);
    free(recv);

    MPI_Finalize();
    return 0;
}
