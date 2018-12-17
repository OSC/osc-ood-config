#PBS -N ondemand/sys/myjobs/basic_omp
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn=28
#PBS -j oe

# This example uses 1 node with 28 cores, which is suitable for Owens. A program must be written to take advantage
# of multithreading for this to work.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

export OMP_NUM_THREADS=28

#
# Move to the directory where the job was submitted
#
cp $PBS_O_WORKDIR/* $TMPDIR
cd $TMPDIR
#
# Run omp job
#
icc -O2 -qopenmp omp-hello.c -o omp-hello
./omp-hello > my_results
#
# Now, copy data (or move) back once the simulation has completed
#
cp my_results $PBS_O_WORKDIR
