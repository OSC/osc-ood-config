#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_omp_mpi
#SBATCH -t 00:10:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=28

# This example is a hybrid MPI/OpenMP job. It runs one MPI process per node with 28 threads per process.
# The assumption here is that the code was written to support multilevel parallelism.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

export OMP_NUM_THREADS=28
export MV2_ENABLE_AFFINITY=0
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
cp hello.c $TMPDIR
cd $TMPDIR
#
# Run job
#
mpicc -O2 -qopenmp hello.c -o hello
./hello > my_results
#
# Now, copy data (or move) back once the simulation has completed
#
cp my_results $SLURM_SUBMIT_DIR
