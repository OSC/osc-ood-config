#!/bin/bash
#SBATCH --job-name="Simple MPI job"
#SBATCH -J ondemand/sys/myjobs/simple_mpi_slurm
#SBATCH -t 00:10:00
#SBATCH --output=mpi-hello.out
#SBATCH --nodes=4

#
# Load MPI module
#
module load intelmpi

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR

#
# Compile mpi-hello.c
#
mpicc mpi-hello.c -o mpi-hello

#
# Run mpi-hello
#
srun --mpi=pmi2 ./mpi-hello
