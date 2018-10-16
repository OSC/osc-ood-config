#PBS -N #PBS -N ondemand/sys/myjobs/basic_omp_mpi
#PBS -l walltime=00:10:00
#PBS -l nodes=4:ppn=28
#PBS -j oe

# This example is a hybrid MPI/OpenMP job. It runs one MPI process per node with 28 threads per process.
# The assumption here is that the code was written to support multilevel parallelism.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts

export OMP_NUM_THREADS=28
export MV2_ENABLE_AFFINITY=0
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
cp hello.c $TMPDIR
cd $TMPDIR
#
# Run job
#
mpicc -O2 -qopenmp hello.c -o hello
./hello > my_results
#
# Now, copy data (or move) back once the simulation has completed
#
cp my_results $PBS_O_WORKDIR
