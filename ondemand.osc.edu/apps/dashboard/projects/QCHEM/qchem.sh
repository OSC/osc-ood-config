#!/bin/bash

#
# This is a sample script for running a basic Q-Chem job.
# The only thing you need to modify is 'sample' here
#
export INPUTFILENAME="sample"

#
# replace 'sample' with the actual name of your input file.
#
module load intel
module load mvapich2
module load qchem

# copy input file to $TMPDIR
cp $INPUTFILENAME.inp $TMPDIR
cd $TMPDIR

# QChem guide at
#   http://www.q-chem.com/qchem-website/manual/qchem43_manual/sect-running.html
#
# Not all calculation types can be run in parallel with MPI.
#
# Temporary hack to get multinode jobs running - it is not yet
# known whether multinode qchem requires a global filesystem.
# setenv QCLOCALSCR $TMPDIR
# export QCSCRATCH=$TMPDIR

qchem -np $SLURM_NTASKS $INPUTFILENAME.inp
ls -al 
