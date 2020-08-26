#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH -J ondemand/sys/myjobs/basic_r_parallel

#  A Basic R Parallel Job for the OSC Pitzer Cluster
#  https://www.osc.edu/resources/available_software/software_list/r

#
# The following lines set up the R environment
#
module load intel/18.0.3
module load openmpi/1.10.7
module load R/3.5.2

#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
# parallel R: submit job with one MPI master
srun R --slave < parallel_testing.R