#!/bin/bash
#SBATCH -J ondemand/sys/myjobs/basic_namd_parallel
#SBATCH --nodes=2
#SBATCH --time=00:12:00
#SBATCH --exclusive

#   A Basic NAMD Parallel Job for the OSC Pitzer Cluster
#   https://www.osc.edu/resources/available_software/software_list/namd

#
# The following lines set up the NAMD environment
#
module load intel/18.0.3  
module load mvapich2/2.3
module load namd/2.13b2
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
sbcast -p apoa1.namd *.xplor apoa1.psf apoa1.pdb $TMPDIR
cd $TMPDIR
#
# Run NAMD
#
run_namd apoa1.namd
#
# Now, copy data (or move) back once the simulation has completed
#
sgather '*' $SLURM_SUBMIT_DIR