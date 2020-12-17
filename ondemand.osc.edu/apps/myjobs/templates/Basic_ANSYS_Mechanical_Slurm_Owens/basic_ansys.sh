#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_ansys_mechanical
#SBATCH --time=00:10:00
#SBATCH -N 1
#SBATCH --licenses=ansys@osc:1

# A basic Ansys Mechanical Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/ansys_mechanical

#
# The following lines set up the ansys environment
#
# For the input file to be read correctly this is the latest working version.
#
module load ansys/19.1
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp $SLURM_SUBMIT_DIR/ansys.in .
#
# Run ansys
#
ansys < ansys.in
#
# Now, copy data (or move) back once the simulation has completed
#
cp * $SLURM_SUBMIT_DIR
