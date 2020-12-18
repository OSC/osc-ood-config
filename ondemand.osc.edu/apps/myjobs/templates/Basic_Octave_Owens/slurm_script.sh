#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_octave
#SBATCH -N 1 -n 28
#SBATCH --time=00:10:00

#   A Basic Octave Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/octave

# load Octave module
module load intel/16.0.8 octave/4.0.3

# copy Octave script to TMPDIR
cd $SLURM_SUBMIT_DIR
cp mycode.o $TMPDIR
cd $TMPDIR

# run Octave script
octave < mycode.o > data.out

# copy output back to original directory
cp data.out $SLURM_SUBMIT_DIR
