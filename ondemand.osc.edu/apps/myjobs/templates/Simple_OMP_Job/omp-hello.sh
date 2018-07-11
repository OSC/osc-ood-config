#PBS -N my_job
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn=28
#PBS -j oe

# This example uses 1 node with 28 cores, which is suitable for Oakley. A similar job on Oakley would use 12 cores;
# the OMP_NUM_THREADS environment variable would also be set to 12. A program must be written to take advantage
# of multithreading for this to work.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

cp $PBS_O_WORKDIR/* $TMPDIR
cd $TMPDIR
export OMP_NUM_THREADS=28
icc -O2 -qopenmp omp-hello.c -o omp-hello
./omp-hello > my_results
cp my_results $PBS_O_WORKDIR
