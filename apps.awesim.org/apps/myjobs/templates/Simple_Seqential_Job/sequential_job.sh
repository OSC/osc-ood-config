#PBS -N simple_sequential
#PBS -l walltime=00:01:00
#PBS -l nodes=1:ppn=1
#PBS -j oe

# The following is an example of a single-processor sequential job that uses $TMPDIR as its working area.
# This batch script copies the script file and input file from the directory the
# qsub command was called from into $TMPDIR, runs the code in $TMPDIR,
# and copies the output file back to the original directory.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

cd $PBS_O_WORKDIR

cp myscript.sh message.in $TMPDIR

cd $TMPDIR

/usr/bin/time ./myscript.sh

cp message.out $PBS_O_WORKDIR
