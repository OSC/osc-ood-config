#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_matlab
#SBATCH --time=00:10:00
#SBATCH --nodes=1


#  A Basic MATLAB Job for the OSC Pitzer Cluster
#  https://www.osc.edu/resources/available_software/software_list/matlab

#
# The following lines set up the Matlab environment
#
module load matlab
#
# Transfer MATLAB script file to TMPDIR
#
cd $SLURM_SUBMIT_DIR
cp hello.m $TMPDIR
cd $TMPDIR
#
# run MATLAB script
#
matlab -nodisplay -nodesktop < hello.m
