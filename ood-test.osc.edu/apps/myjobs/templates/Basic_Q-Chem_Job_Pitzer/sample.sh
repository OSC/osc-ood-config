#PBS -N ondemand/sys/myjobs/basic_qchem
#PBS -l walltime=0:59:00
#PBS -S /bin/csh
#PBS -j oe
#PBS -l nodes=2:ppn=40
#
# This is a sample script for running a basic Q-Chem job.
# The only thing you need to modify is 'sample' here:
#
setenv JOBNAME sample
#
# replace 'sample' with the actual name of your input file.
#
module load intel/18.0.4
module load mvapich2/2.3
module load qchem/5.1.1

# copy the contents to TMPDIR
cp $PBS_O_WORKDIR/* $TMPDIR
cd $TMPDIR

# QChem guide at
#   http://www.q-chem.com/qchem-website/manual/qchem43_manual/sect-running.html
#
# Not all calculation types can be run in parallel with MPI.
#
# Temporary hack to get multinode jobs running - it is not yet
# known whether multinode qchem requires a global filesystem.
cd $PBS_O_WORKDIR
setenv QCSCRATCH $TMPDIR
#setenv QCLOCALSCR $TMPDIR
#
set NPROC = `cat $PBS_NODEFILE | wc -l`
qchem -np ${NPROC} $JOBNAME.inp $JOBNAME.out
cp -p $JOBNAME.out $PBS_O_WORKDIR
cat $JOBNAME.out
ls -al