#PBS -N ondemand/sys/myjobs/basic_cuda_serial
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=1:gpus=1
#PBS -j oe

#   A Basic CUDA Serial Job for the OSC Pitzer Cluster
#   https://www.osc.edu/resources/available_software/software_list/cuda

#
# The following lines set up the COMSOL environment
#
module load cuda
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
cp hello.cu  $TMPDIR
cd $TMPDIR
#
# Compile CUDA Code and create executable
#
nvcc -o hello hello.cu
#
# Run App
#
./hello
#
# Now, copy data (or move) back once the simulation has completed
#
cp * $PBS_O_WORKDIR