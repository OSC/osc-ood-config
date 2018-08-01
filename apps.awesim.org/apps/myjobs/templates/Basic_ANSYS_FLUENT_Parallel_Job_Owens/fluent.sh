#PBS -N parallel_fluent
#PBS -l walltime=00:10:00
#PBS -l nodes=2:ppn=28
#PBS -j oe
#PBS -l software=ansys+1%ansyspar+52
#PBS -S /bin/bash

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
cd $PBS_O_WORKDIR 
cp /users/oscgen/xwang/Fluent/Demo_tmi_fluent/test.* .
#   
# Create list of nodes to launch job on   
rm -f pnodes   
cat  $PBS_NODEFILE | sort > pnodes   
export ncpus=`cat pnodes | wc -l`   
#   
#   Run fluent   
fluent 3d -t$ncpus -pinfiniband.ofed -cnf=pnodes -g < run.input 