#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_ansys_fluent_parallel
#SBATCH -t 00:10:00
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --licenses=ansys@osc:1,ansyspar@osc:52



# A basic FLUENT Parallel Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/fluent

set echo on
hostname
#
# The following lines set up the FLUENT environment
#
module load ansys
#
# Move to the directory where the job was submitted from and
# create the config file for socket communication library
#
cd $SLURM_SUBMIT_DIR
cp /users/oscgen/xwang/software/Fluent/Demo_tmi_fluent/test.* .
#
# Create list of nodes to launch job on
# Create variable to contain amount of ntasks per node
export TASKS_PER_NODE=$(($SLURM_NTASKS/$SLURM_JOB_NUM_NODES))
rm -f pnodes
scontrol show hostnames $SLURM_JOB_NODELIST | sort > tempnodes
while read i; do seq 1 $TASKS_PER_NODE| xargs -i -- printf "%s\n" $i >> pnodes;done < tempnodes
rm -f tempnodes
export ncpus=`cat pnodes  | wc -l`
#
#   Run fluent
fluent 3d -t$ncpus -pinfiniband.ofed -cnf=pnodes -g < run.input
