#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:45:00
#SBATCH -J ondemand/sys/myjobs/basic_blast

# A Basic BLAST Job for the OSC Pitzer Cluster
# https://www.osc.edu/resources/available_software/software_list/blast

#
# The following lines set up the Blast environment
#
module load blast
module load blast-database
set -x
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
mkdir $SLURM_JOBID
cp 100.fasta $TMPDIR
cd $TMPDIR

#
# Run Blast
#
/usr/bin/time tblastn -db nt -query 100.fasta -out test.out
#
# Now, copy data (or move) back once the simulation has completed
#
cp test.out $SLURM_SUBMIT_DIR/$SLURM_JOBID
