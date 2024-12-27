#!/bin/bash
#SBATCH --job-name="Simple OpenMP job"
#SBATCH -J ondemand/sys/myjobs/omp_job_slurm
#SBATCH --output=omp-hello.out
#SBATCH -t 00:01:00
#SBATCH --nodes=1

# Load the OpenMPI module
module load intel/19.0.5
module load openmpi/4.0.3

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
cp omp-hello.c $TMPDIR
cd $TMPDIR

#
# Compile omp-hello.c
#
mpicc -qopenmp omp-hello.c -o omp-hello

#
# Run omp-hello
#
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE
srun --export=ALL -n 1 ./omp-hello
