#!/bin/csh
#SBATCH -J ondemand/sys/myjobs/basic_gaussian
#SBATCH --time=0:30:00
#SBATCH --nodes=1

# A Basic Gaussian Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/gaussian

# SLURM_SUBMIT_DIR refers to the directory from which the job was submitted.

# Emit verbose details as the job script executes.
set echo
set verbose
# Emit verbose details on the job's queuing.
squeue -j $SLURM_JOB_ID

#
# The following lines set up the Gaussian environment
#
module load gaussian/g16a03
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp -p /users/appl/srb/workshops/compchem/gaussian/c80.owens.com .
#
# Run Gaussian
#
g16 < c80.owens.com > c80.owens.com.log
ls -al
#
# Now, copy data (or move) back once the simulation has completed
#
cp -p *.chk $SLURM_SUBMIT_DIR
