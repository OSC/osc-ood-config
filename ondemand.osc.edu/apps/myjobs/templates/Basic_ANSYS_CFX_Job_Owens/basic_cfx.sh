#PBS -N serialjob_cfx
#PBS -l walltime=1:00:00
#PBS -l software=ansys+1
#PBS -l nodes=1:ppn=1
#PBS -j oe
#PBS -S /bin/bash

# A basic CFX Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/cfx

#Set up CFX environment.
module load ansys

#Copy CFX files like .def to $TMPDIR and move there to execute the program
cd $TMPDIR
cp /users/oscgen/xwang/CFX/test.def  .


#Run CFX in serial with test.def as input file
cfx5solve -batch -def test.def 

#Finally, copy files back to your home directory
cp  * $PBS_O_WORKDIR
