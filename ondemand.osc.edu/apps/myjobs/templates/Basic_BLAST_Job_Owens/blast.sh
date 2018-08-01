#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00
#PBS -N ondemand/sys/myjobs/basic_blast
#PBS -S /bin/bash
#PBS -j oe

# A Basic BLAST Job for the OSC Owens Cluster
# https://www.osc.edu/resources/available_software/software_list/blast

#
# The following lines set up the Blast environment
#
module load blast
set -x
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
mkdir $PBS_JOBID
cp 100.fasta $TMPDIR
cd $TMPDIR

#
# Run Blast
#
/usr/bin/time blastn -db nt -query 100.fasta -out test.out
#
# Now, copy data (or move) back once the simulation has completed
#
cp test.out $PBS_O_WORKDIR/$PBS_JOBID
