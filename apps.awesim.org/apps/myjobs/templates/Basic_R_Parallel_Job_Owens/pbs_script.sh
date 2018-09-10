#!/bin/bash
#PBS -l walltime=2:10:00
#PBS -l nodes=2:ppn=28
#PBS -j oe
#PBS -N ondemand/sys/myjobs/basic_r_parallel

#  A Basic R Parallel Job for the OSC Owens Cluster
#  https://www.osc.edu/resources/available_software/software_list/r

#
# The following lines set up the R environment
#
module load openmpi/1.10
module load R/3.3.1

#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
# parallel R: submit job with one MPI master
mpirun -np 1 R --slave < parallel_testing.R