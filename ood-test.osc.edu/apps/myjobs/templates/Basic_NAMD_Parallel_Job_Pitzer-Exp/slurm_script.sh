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
module load intel/19.0.5  
module load mvapich2/2.3.4
module load namd/2.13
#
# Move to the directory where the job was submitted
#
cd $SLURM_SUBMIT_DIR
sbcast -p apoa1.namd $TMPDIR/apoa1.namd
sbcast -p par_all22_popc.xplor $TMPDIR/par_all22_popc.xplor
sbcast -p par_all22_prot_lipid.xplor $TMPDIR/par_all22_prot_lipid.xplor
sbcast -p apoa1.psf $TMPDIR/apoa1.psf
sbcast -p apoa1.pdb $TMPDIR/apoa1.pdb
cd $TMPDIR
#
# Run NAMD
#
namd2 apoa1.namd
