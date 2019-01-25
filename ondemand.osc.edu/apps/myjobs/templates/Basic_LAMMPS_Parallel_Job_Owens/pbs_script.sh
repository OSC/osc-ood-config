#PBS -N ondemand/sys/myjobs/basic_lammps_parallel
#PBS -j oe
#PBS -l walltime=1:00:00
#PBS -l nodes=2:ppn=28
#PBS -S /bin/bash

#  A Basic LAMMPS Parallel Job for the OSC Owens cluster
# https://www.osc.edu/resources/available_software/software_list/lammps

# emit verbose details on the job's queuing.
qstat -f $PBS_JOBID
#
# The following lines set up the LAMMPS environment
#
module load lammps
module list
export OMP_NUM_THREADS=56
export MV2_ENABLE_AFFINITY=0
#
# Move to the directory where the job was submitted
#
pbsdcp -p /users/appl/srb/workshops/compchem/lammps/in.crack $PBS_O_WORKDIR
cd $PBS_O_WORKDIR
pbsdcp -p in.crack $TMPDIR
cd $TMPDIR
#
# Run LAMMPS
#
lammps < in.crack
#
# Now, copy data (or move) back once the simulation has completed
#
pbsdcp -pg '*' $PBS_O_WORKDIR
ls -al
