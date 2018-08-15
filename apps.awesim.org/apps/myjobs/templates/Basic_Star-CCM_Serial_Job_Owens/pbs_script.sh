#PBS -N ondemand/sys/myjobs/basic_starccm_serial
#PBS -l walltime=00:30:00
#PBS -l nodes=1:ppn=1
#PBS -l software=starccm+1
#PBS -j oe
#PBS -S /bin/bash

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
cp /users/oscgen/xwang/STAR-CCM+/elbow.sim .
#
# Run Star-CCM+
#
starccm+ -batch elbow.sim >&output.txt
#
# Now, copy data (or move) back once the simulation has completed
#
cp output.txt $PBS_O_WORKDIR
