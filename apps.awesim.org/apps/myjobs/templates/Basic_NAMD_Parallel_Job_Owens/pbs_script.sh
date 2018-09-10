#!/bin/bash
#PBS -N ondemand/sys/myjobs/basic_namd_parallel
#PBS -l nodes=2:ppn=28
#PBS -l walltime=0:12:00
#PBS -S /bin/bash
#PBS -j oe

#   A Basic NAMD Parallel Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/namd

#
# The following lines set up the NAMD environment
#
module load namd/2.12
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
pbsdcp -p apoa1.namd *.xplor apoa1.psf apoa1.pdb $TMPDIR
cd $TMPDIR
#
# Run NAMD
#
run_namd apoa1.namd
#
# Now, copy data (or move) back once the simulation has completed
#
pbsdcp -g '*' $PBS_O_WORKDIR