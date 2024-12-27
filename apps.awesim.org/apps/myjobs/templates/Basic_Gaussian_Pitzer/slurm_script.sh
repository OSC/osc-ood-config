#!/bin/csh
#SBATCH -J ondemand/sys/myjobs/basic_gaussian
#SBATCH --time=00:30:00
#SBATCH --nodes=1

# A Basic Gaussian Job for the OSC Pitzer Cluster
#   https://www.osc.edu/resources/available_software/software_list/gaussian

# SLURM_SUBMIT_DIR refers to the directory from which the job was submitted.

#
# The following lines set up the Gaussian environment
# User must be a member of GaussC for usage
#
module load gaussian
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp -p /users/appl/srb/workshops/compchem/gaussian/glucose.com .
#
# Run Gaussian
#
g16 <glucose.com >glucose.log
ls -al
#
# Now, copy data (or move) back once the simulation has completed
#
cp -p glucose.log glucose.chk $SLURM_SUBMIT_DIR
