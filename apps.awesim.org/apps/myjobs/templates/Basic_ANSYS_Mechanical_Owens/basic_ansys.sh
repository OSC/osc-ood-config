#PBS -N ondemand/sys/myjobs/basic_ansys_mechanical
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=1
#PBS -l software=ansys+1
#PBS -j oe

# A basic Ansys Mechanical Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/ansys_mechanical

#
# The following lines set up the ansys environment
#
module load ansys
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp $PBS_O_WORKDIR/ansys.in .
#
# Run ansys
#
ansys < ansys.in
#
# Now, copy data (or move) back once the simulation has completed
#
cp * $PBS_O_WORKDIR
