#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_ansys_fluent_serial
#SBATCH --time=00:30:00
#SBATCH -N 1
#SBATCH --licenses=ansys@osc:1

# A basic FLUENT Serial Job
# Further details available at:
# 	https://www.osc.edu/resources/available_software/software_list/ansys/fluent

#
# The following lines set up the FLUENT environment
#
module load ansys
#
# Move to the directory where the job was submitted from
# You could also 'cd' directly to your working directory
cd 	$SLURM_SUBMIT_DIR
#
# Copy files to $TMPDIR and move there to execute the program
#
cp /users/oscgen/xwang/software/Fluent/Demo_tmi_fluent/test.* run.input $TMPDIR
cd $TMPDIR
#
# Run fluent
fluent 3d -g < run.input
#
# Where the file 'run.input' contains the commands you would normally
# type in at the Fluent command prompt.
# Finally, copy files back to your home directory
cp * $SLURM_SUBMIT_DIR
