#PBS -N ondemand/sys/myjobs/basic_parallel
#PBS -l walltime=00:10:00
#PBS -l nodes=4:ppn=28
#PBS -j oe

# Here is an example of an MPI job that uses 4 nodes with 28 cores each, running one process per core
# (112 processes total). 
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

#
# Move to the directory where the job was submitted
#
cp $PBS_O_WORKDIR/* $TMPDIR
cd $TMPDIR
export OMP_NUM_THREADS=28
#
# Run parallel job
#
mpicc -O2 myscript.c -o myscript
./myscript > my_results
#
# Now, copy data (or move) back once the simulation has completed
#
cp my_results $PBS_O_WORKDIR