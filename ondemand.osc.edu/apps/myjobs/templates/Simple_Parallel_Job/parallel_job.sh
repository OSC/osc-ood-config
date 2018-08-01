#PBS -N myscript
#PBS -l walltime=00:10:00
#PBS -l nodes=4:ppn=28
#PBS -j oe

# Here is an example of an MPI job that uses 4 nodes with 28 cores each, running one process per core
# (112 processes total). This assumes a.out was built with the gnu compiler in order to illustrate the
# module command. The module swap is necessary on Owens when running MPI programs built with a
# compiler other than Intel.
#   https://www.osc.edu/supercomputing/batch-processing-at-osc/job-scripts
module load openmpi

cp $PBS_O_WORKDIR/* $TMPDIR
cd $TMPDIR
export OMP_NUM_THREADS=28
mpicc -O2 myscript.c -o myscript
./myscript > my_results
cp my_results $PBS_O_WORKDIR