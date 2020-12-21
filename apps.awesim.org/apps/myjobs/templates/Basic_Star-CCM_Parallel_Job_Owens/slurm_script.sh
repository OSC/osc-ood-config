#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_starccm_parallel
#SBATCH --time=00:30:00
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --licenses=starccm@osc:1,starccmpar@osc:56


#   A Basic Star-CCM+ Parallel Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/star_ccm
#
# The following lines set up the Star-CCM+ environment
#
module load starccm
#
# Move to the directory where the job will run
#
cd $SLURM_SUBMIT_DIR
rm -f tempnodes
rm -f pnodes
cp /users/oscgen/xwang/software/STAR-CCM+/elbow.sim .
scontrol show hostnames $SLURM_JOB_NODELIST | sort > tempnodes
#
# Run Star-CCM+
#
starccm+ -np 56 -batch -machinefile tempnodes -mpi intel -mpiflags '-rmk slurm' -rsh ssh elbow.sim >&output.txt
