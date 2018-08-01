#PBS -N AppNameJob
#PBS -l nodes=1:ppn=12
#PBS -l walltime=01:00:00
#PBS -l software=appname

#   A Basic Octave Job for the OSC Oakley Cluster
#   https://www.osc.edu/resources/available_software/software_list/octave

module load octave

cd $PBS_O_WORKDIR

cp mycode.o $TMPDIR

cd $TMPDIR

octave < mycode.o > data.out

cp data.out $PBS_O_WORKDIR
