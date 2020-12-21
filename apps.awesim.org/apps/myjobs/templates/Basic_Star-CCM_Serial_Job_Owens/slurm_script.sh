#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_starccm_serial
#SBATCH --time=00:30:00
#SBATCH -N 1
#SBATCH --licenses=starccm@osc:1

#   A Basic Star-CCM+ Serial Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/star_ccm
#
# The following lines set up the Star-CCM+ environment
#
module load starccm
#
# Move to the directory where the job will run
#
cd $TMPDIR
cp /users/oscgen/xwang/software/STAR-CCM+/elbow.sim .
#
# Run Star-CCM+
#
starccm+ -batch elbow.sim >&output.txt
#
# Now, copy data (or move) back once the simulation has completed
#
cp output.txt $SLURM_SUBMIT_DIR
