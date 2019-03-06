#PBS -l walltime=0:30:00
#PBS -l nodes=2:ppn=28
#PBS -N ondemand/sys/myjobs/basic_comsol_parallel
#PBS -j oe
#PBS -r n
#PBS -l software=comsolscript

#  A Basic COMSOL Parallel Job for the OSC Owens Cluster
#  https://www.osc.edu/resources/available_software/software_list/comsol

#
# The following lines set up the COMSOL environment
#
module load comsol
#
# Move to the directory where the job was submitted
#
cd ${PBS_O_WORKDIR}
echo "--- Copy Input Files to TMPDIR and Change Disk to TMPDIR"
cp /usr/local/comsol/comsol52a/demo/api/beammodel/BeamModel.mph $TMPDIR
cd $TMPDIR
np=28
echo "--- Running on ${np} processes (cores) on the following nodes:"
cat $PBS_NODEFILE | uniq > hostfile
#
# Run COMSOL
#
echo "--- COMSOL run"
comsol -nn 2 -np ${np} batch -f hostfile -mpirsh ssh -inputfile BeamModel.mph -outputfile output.mph
#
# Now, copy data (or move) back once the simulation has completed
#
echo "--- Copy files back"
cp output.mph output.mph.status ${PBS_O_WORKDIR}
echo "---Job finished at: 'date'"
echo "---------------------------------------------"
