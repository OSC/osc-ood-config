#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH -N 2 -n 28
#SBATCH --job-name=ondemand/sys/myjobs/basic_r_parallel

#  A Basic R Parallel Job for the OSC Owens Cluster
#  https://www.osc.edu/resources/available_software/software_list/r

#
# The following lines set up the R environment
#
module load intel/16.0.3
module load openmpi/1.10.5
module load R/3.3.1

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
# parallel R: submit job with one MPI master
mpirun -np 1 R --slave < parallel_testing.R
