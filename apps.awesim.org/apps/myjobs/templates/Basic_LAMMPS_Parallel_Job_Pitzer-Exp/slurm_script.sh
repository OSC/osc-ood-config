#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_lammps_parallel
#SBATCH --time=00:30:00
#SBATCH --nodes=2 
#SBATCH --ntasks-per-node=40
#SBATCH -S /bin/bash

#  A Basic LAMMPS Parallel Job for the OSC Pitzer cluster
# https://www.osc.edu/resources/available_software/software_list/lammps

# emit verbose details on the job's queuing.
scontrol show job $SLURM_JOBID
#
# The following lines set up the LAMMPS environment
#
module load lammps
module list
export OMP_NUM_THREADS=80 # this must match nodes * ppn
#
# Move to the directory where the job was submitted
#
sbcast -p /users/appl/srb/workshops/compchem/lammps/in.crack $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR
sbcast -p in.crack $TMPDIR
cd $TMPDIR
#
# Run LAMMPS
#
lammps < in.crack
#
# Now, copy data (or move) back once the simulation has completed
#
sgather -p '*' $SLURM_SUBMIT_DIR
ls -al
