#PBS -N simple_abaqus
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=1
#PBS -l software=abaqus+5
#PBS -j oe

# set up the ABAQUS environment
module load abaqus

# move to the directory where the job was submitted
cd $PBS_O_WORKDIR
cp *.inp $TMPDIR
cd $TMPDIR

# run ABAQUS
abaqus job=sample_job input=knee_bolster.inp interactive

# copy data back once the simulation has completed
cp * $PBS_O_WORKDIR