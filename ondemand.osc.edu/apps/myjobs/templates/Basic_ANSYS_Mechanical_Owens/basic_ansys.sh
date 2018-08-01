#PBS -N ansys_test
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=1
#PBS -l software=ansys+1
#PBS -j oe

# A basic Ansys Mechanical Job
# Further details at:
#	https://www.osc.edu/resources/available_software/software_list/ansys/ansys_mechanical

cd $TMPDIR
cp $PBS_O_WORKDIR/ansys.in .
module load ansys
ansys < ansys.in
cp * $PBS_O_WORKDIR
