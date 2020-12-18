#SBATCH --job-name=ondemand/sys/myjobs/basic_abaqus
#SBATCH --time=00:45:00
#SBATCH -N 1 -n 1
#SBATCH --licenses=abaqus@osc:5
#
# A Basic Abaqus Job for the OSC Owens Cluster
# https://www.osc.edu/resources/available_software/software_list/abaqus
#
# The following lines set up the ABAQUS environment
#
module load abaqus
#
# Move to the work directory
#
cd $SLURM_SUBMIT_DIR
#
# Fetch input files
#
abaqus fetch job=knee_bolster
abaqus fetch job=knee_bolster_ef1
abaqus fetch job=knee_bolster_ef2
abaqus fetch job=knee_bolster_ef3
#
# Copy input files from work directory($PBS_O_WORKDIR) to $TMPDIR
#
cp *.inp $TMPDIR
#
# Move to $TMPDIR
#
cd $TMPDIR
#
# Run ABAQUS
#
abaqus job=knee_bolster interactive
#
# Now, copy data (or move) back once the simulation has completed
#
cp * $SLURM_SUBMIT_DIR
