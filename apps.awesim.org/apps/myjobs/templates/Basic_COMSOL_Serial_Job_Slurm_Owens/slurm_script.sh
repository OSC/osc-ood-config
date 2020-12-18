#!/bin/bash 
#SBATCH --job-name=ondemand/sys/myjobs/basic_comsol_serial
#SBATCH --time=00:30:00
#SBATCH -N 1
#SBATCH --licenses=comsolscript@osc

#   A Basic COMSOL Serial Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/comsol

#
# The following lines set up the COMSOL environment
#
module load comsol
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
cp /usr/local/comsol/comsol52a/demo/api/beammodel/BeamModel.mph $TMPDIR
cd $TMPDIR
#
# Run COMSOL
#
comsol batch -inputfile BeamModel.mph
#
# Now, copy data (or move) back once the simulation has completed
#
cp * $SLURM_SUBMIT_DIR
