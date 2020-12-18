#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_ansys_cfx
#SBATCH --time=00:10:00
#SBATCH --licenses=ansys@osc:1
#SBATCH -N 1

# A basic CFX Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/cfx

#Set up CFX environment.
module load ansys

#Copy CFX files like .def to $TMPDIR and move there to execute the program
cd $TMPDIR
cp /users/oscgen/xwang/software/CFX/test.def  .


#Run CFX in serial with test.def as input file
cfx5solve -batch -def test.def

#Finally, copy files back to your home directory
cp  * $SLURM_SUBMIT_DIR
