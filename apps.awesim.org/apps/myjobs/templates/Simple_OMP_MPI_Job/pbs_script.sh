#PBS -N my_job
#PBS -l walltime=00:10:00
#PBS -l nodes=4:ppn=28
#PBS -j oe

# This example is a hybrid MPI/OpenMP job. It runs one MPI process per node with 28 threads per process.
# The assumption here is that the code was written to support multilevel parallelism.
# The executable is named hybridprogram.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

export OMP_NUM_THREADS=28
export MV2_ENABLE_AFFINITY=0

cd $PBS_O_WORKDIR

cp hello.c $TMPDIR

cd $TMPDIR
mpicc -O2 -qopenmp hello.c -o hello
./hello > my_results
cp my_results $PBS_O_WORKDIR
