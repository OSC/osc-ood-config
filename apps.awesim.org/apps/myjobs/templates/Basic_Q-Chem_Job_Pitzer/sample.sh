<<<<<<< Updated upstream
#!/bin/csh
#SBATCH -J ondemand/sys/myjobs/basic_qchem
#SBATCH --time=00:30:00
#SBATCH --exclusive
#SBATCH --nodes=2
=======
#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_qchem_slurm
#SBATCH --nodes=1
#SBATCH --tasks-per-node 40
#SBATCH	--time=00:30:00
#SBATCH --exclusive
#SBATCH --output=job-output

>>>>>>> Stashed changes
#
# This is a sample script for running a basic Q-Chem job.
# The only thing you need to modify is 'sample' here
#
export INPUTFILENAME="sample"
#
# replace 'sample' with the actual name of your input file.
#
<<<<<<< Updated upstream
module load intel/18.0.4
module load mvapich2/2.3
module load qchem/5.3

# copy the contents to TMPDIR
cp $SLURM_SUBMIT_DIR/* $TMPDIR
=======
module load intel
module load mvapich2
module load qchem

# copy input file to $TMPDIR
cp $INPUTFILENAME.inp $TMPDIR
>>>>>>> Stashed changes
cd $TMPDIR

# QChem guide at
#   http://www.q-chem.com/qchem-website/manual/qchem43_manual/sect-running.html
#
# Not all calculation types can be run in parallel with MPI.
#
# Temporary hack to get multinode jobs running - it is not yet
# known whether multinode qchem requires a global filesystem.
<<<<<<< Updated upstream
cd $SLURM_SUBMIT_DIR
setenv QCSCRATCH $TMPDIR
#setenv QCLOCALSCR $TMPDIR
#
set NPROC = `cat $SLURM_JOB_NODELIST | wc -l`
qchem -np ${NPROC} $JOBNAME.inp $JOBNAME.out
cp -p $JOBNAME.out $SLURM_SUBMIT_DIR
cat $JOBNAME.out
ls -al
=======
# export QCSCRATCH=$TMPDIR

qchem -np $SLURM_NPROCS $INPUTFILENAME.inp  
ls -al 

>>>>>>> Stashed changes
