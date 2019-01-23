#!/bin/bash
#PBS -l walltime=2:10:00
#PBS -l nodes=2:ppn=40
#PBS -j oe
#PBS -N ondemand/sys/myjobs/basic_r_parallel

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
cd $PBS_O_WORKDIR
# parallel R: submit job with one MPI master
mpirun -np 1 R --slave < parallel_testing.R