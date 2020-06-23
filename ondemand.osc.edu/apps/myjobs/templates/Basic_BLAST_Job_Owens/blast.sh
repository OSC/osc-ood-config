#!/bin/bash
#PBS -N "rfm_blast_tblast_example_job"
#PBS -o rfm_blast_tblast_example_job.out
#PBS -e rfm_blast_tblast_example_job.err
#PBS -l walltime=0:10:0
#PBS -A PZS0710
#PBS -l nodes=1:ppn=28
#PBS -q debug

cd $PBS_O_WORKDIR
module load blast-database/2018-08
module load blast


# Check module environment
module list
echo MODULEPATH=$MODULEPATH 1>&2

 
#
# Copy input data to the fast file system
#
cp 100.fasta $TMPDIR
cd $TMPDIR

#
# Run tblastn with 16 threads
# compares a protein query sequence against a nucleotide sequence database
# dynamically translated in all six reading frames (both strands).
#
tblastn -db nt -query 100.fasta -num_threads 16 -out 100_tblastn.out

#
# Now, copy data (or move) back once the simulation has completed
#
cp 100_tblastn.out $PBS_O_WORKDIR/


