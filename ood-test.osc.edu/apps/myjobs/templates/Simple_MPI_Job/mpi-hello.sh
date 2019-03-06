#PBS -N ondemand/sys/myjobs/basic_mpi
#PBS -l walltime=00:10:00
#PBS -l nodes=4:ppn=28
#PBS -j oe
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
#
# Build mpi job with compiler wrapper
#
mpicc -O2 mpi-hello.c -o mpi-hello
#
# Run mpi job
#
mpiexec ./mpi-hello

