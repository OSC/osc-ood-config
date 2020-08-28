#!/bin/bash

#SBATCH --job-name="Simple OpenMP job"
#SBATCH -J ondemand/sys/myjobs/omp_job_slurm
#SBATCH --output=omp-hello.out
#SBATCH -t 00:01:00
#SBATCH --nodes=1
#SBATCH --exclusive

# Load the OpenMPI module
module load openmpi

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
cp omp-hello.c $TMPDIR
cd $TMPDIR

#
# Compile omp-hello.c
#
mpicc omp-hello.c -o omp-hello

#
# Run omp-hello
#
srun ./omp-hello