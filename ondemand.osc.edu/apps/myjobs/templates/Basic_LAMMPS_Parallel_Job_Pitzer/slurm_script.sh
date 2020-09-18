#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_lammps_parallel
#SBATCH --time=00:30:00
#SBATCH --nodes=2

#  A Basic LAMMPS Parallel Job for the OSC Pitzer cluster
# https://www.osc.edu/resources/available_software/software_list/lammps

# emit verbose details on the job's queuing.
scontrol show job $SLURM_JOBID

#
# The following lines set up the LAMMPS environment
#
module load intel/19.0.5 mvapich2/2.3.4 lammps/3Mar20

#
# Move to the directory where the job was submitted
#

cd $TMPDIR
sbcast -p /users/appl/srb/workshops/compchem/lammps/in.crack $TMPDIR/in.crack

#
# Run LAMMPS
#
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE
srun --export=ALL -n 2 lammps < $TMPDIR/in.crack
