#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_cuda_serial
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --gpus=1


#   A Basic CUDA Serial Job for the OSC Pitzer Cluster
#   https://www.osc.edu/resources/available_software/software_list/cuda

#
# The following lines set up the COMSOL environment
#
module load cuda
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
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
cp * $SLURM_SUBMIT_DIR