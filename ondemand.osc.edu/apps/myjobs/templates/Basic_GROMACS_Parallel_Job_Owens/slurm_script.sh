# Owens example batch script for GROMACS 2018 using the non MPI, non GPU mdrun;
# thus nodes must be 1 and only OpenMP based parallelism is used.
# GROMACS Tutorial of Lysozyme step 8 production MD :
# http://www.bevanlab.biochem.vt.edu/Pages/Personal/justin/gmx-tutorials/lysozyme/index.html
#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_gromacs_parallel
#SBATCH --time=00:30:00
#SBATCH -N 1 -n 28

#  A Basic GROMACS Serial Job for the OSC Owens Cluster
#  https://www.osc.edu/resources/available_software/software_list/gromacs

# turn off verbosity for noisy module commands
set +vx

#
# The following lines set up the environment
#
module unload mvapich2
module unload intel
module load intel/18.0.3
module load mvapich2/2.3
module load gromacs/2018.2
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
