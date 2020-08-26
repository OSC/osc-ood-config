#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_gromacs_parallel
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --exclusive

#  A Basic GROMACS Serial Job for the OSC Pitzer Cluster
#  https://www.osc.edu/resources/available_software/software_list/gromacs

# turn off verbosity for noisy module commands
set +vx

#
# The following lines set up the environment
#
module purge
module load intel/18.0.4 mvapich2/2.3 gromacs/2018.2
module list
set -vx

sbcast -p /users/appl/srb/workshops/compchem/gromacs/md01.tpr $TMPDIR
# Use TMPDIR for best performance.
cd $TMPDIR
#
# Run GROMACS
#
gmx mdrun -deffnm md01
cat md01.log
#
# Now, copy data (or move) back once the simulation has completed
#
cp -p * $SLURM_SUBMIT_DIR/
ls -al