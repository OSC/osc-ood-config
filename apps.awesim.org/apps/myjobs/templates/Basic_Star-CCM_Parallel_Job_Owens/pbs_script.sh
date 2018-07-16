#PBS -N starccm_test 
#PBS -l walltime=3:00:00 
#PBS -l nodes=2:ppn=28
#PBS -l software=starccm+1%starccmpar+56
#PBS -j oe
#PBS -S /bin/bash

#   A Basic Star-CCM+ Parallel Job for the OSC Owens Cluster
#   https://www.osc.edu/supercomputing/software/star_ccm

cd $PBS_O_WORKDIR

cp starccm.sim $TMPDIR

cd $TMPDIR

module load starccm

starccm+ -np 56 -batch -machinefile $PBS_NODEFILE starccm.sim > output.txt

cp output.txt $PBS_O_WORKDIR
