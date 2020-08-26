#PBS -N ondemand/sys/myjobs/basic_sequential
#PBS -l walltime=00:01:00
#PBS -l nodes=1:ppn=1
#PBS -j oe

# The following is an example of a single-processor sequential job that uses $TMPDIR as its working area.
# This batch script copies the script file and input file from the directory the
# qsub command was called from into $TMPDIR, runs the code in $TMPDIR,
# and copies the output file back to the original directory.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
cp myscript.sh message.in $TMPDIR
cd $TMPDIR
#
# Run sequential job
#
/usr/bin/time ./myscript.sh
#
# Now, copy data (or move) back once the simulation has completed
#
cp message.out $PBS_O_WORKDIR
