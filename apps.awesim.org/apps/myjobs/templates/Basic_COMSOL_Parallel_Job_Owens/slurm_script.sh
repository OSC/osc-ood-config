#!/bin/bash
#SBATCH --time=0:30:00
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --job-name=ondemand/sys/myjobs/basic_comsol_parallel
#SBATCH --no-requeue
#SBATCH --licenses=comsolscript@osc

#  A Basic COMSOL Parallel Job for the OSC Owens Cluster
#  https://www.osc.edu/resources/available_software/software_list/comsol

#
# The following lines set up the COMSOL environment
#
module load comsol
#
# Move to the directory where the job was submitted
#
cd ${SLURM_SUBMIT_DIR}
echo "--- Copy Input Files to TMPDIR and Change Disk to TMPDIR"
cp /usr/local/comsol/comsol52a/demo/api/beammodel/BeamModel.mph $TMPDIR
cd $TMPDIR
np=28
echo "--- Running on ${np} processes (cores) on the following nodes:"
scontrol show hostnames $SLURM_JOB_NODELIST | uniq > hostfile
#
# Run COMSOL
#
echo "--- COMSOL run"
comsol -nn 2 -np ${np} batch -f hostfile -mpirsh ssh -inputfile BeamModel.mph -outputfile output.mph
#
# Now, copy data (or move) back once the simulation has completed
#
echo "--- Copy files back"
cp output.mph output.mph.status ${SLURM_SUBMIT_DIR}
echo "---Job finished at: 'date'"
echo "---------------------------------------------"
