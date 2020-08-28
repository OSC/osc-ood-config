#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_amber
#SBATCH --time=00:10:00
#SBATCH --nodes=2
#SBATCH --exclusive
#
# The following lines set up the Amber environment
# Further Details at
#	https://www.osc.edu/resources/available_software/software_list/amber
#
set echo
# emit verbose details on the job's queuing.
scontrol show job $SLURM_JOBID
module load intel/17.0.7  mvapich2/2.3 amber/18
echo "AMBERHOME=$AMBERHOME"
#
# SLURM_SUBMIT_DIR refers to the directory from which the job was submitted.
echo "SLURM_SUBMIT_DIR=$SLURM_SUBMIT_DIR"
cd $TMPDIR
#
# The file names below may need to be changed
cp -p /users/appl/srb/workshops/compchem/amber/mdin .
cp -p /users/appl/srb/workshops/compchem/amber/prmtop .
cp -p /users/appl/srb/workshops/compchem/amber/inpcrd.equil .
#
# Some jobs may require the -O option on the Amber command lines below
#mpiexec $AMBERHOME/bin/sander.MPI -i $MDIN -o stdout -inf $MDINFO -p $PRMTOP -c $INPCRD -ref $REFC -x $MDCRD -v $MDVEL -e $MDEN -r $RESTRT
# Some jobs may use pmemd which consumes less walltime than sander.
srun $AMBERHOME/bin/pmemd.MPI -i mdin -o mdout -p prmtop -c inpcrd.equil
ls -al
cp -p mdout $SLURM_SUBMIT_DIR
cat mdout