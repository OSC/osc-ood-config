#!/bin/sh

#SBATCH --job-name="Simple Parallel job"
#SBATCH -J ondemand/sys/myjobs/simple_parallel_slurm
#SBATCH -t 00:10:00
#SBATCH --output=myscript.out
#SBATCH --partition=parallel
#SBATCH --nodes=4
#SBATCH --exclusive

#
# Load MPI module
#
module load intelmpi

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR

#
# Compile myscript.c
#
mpicc myscript.c -o myscript

#
# Run myscript
#
srun ./myscript







