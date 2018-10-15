#PBS -N basic_octave
#PBS -l nodes=1:ppn=12
#PBS -l walltime=00:10:00
#PBS -l software=octave

#   A Basic Octave Job for the OSC Oakley Cluster
#   https://www.osc.edu/resources/available_software/software_list/octave

# load Octave module
module load octave

# copy Octave script to TMPDIR
cd $PBS_O_WORKDIR
cp mycode.o $TMPDIR
cd $TMPDIR

# run Octave script
octave < mycode.o > data.out


# copy output back to original directory
cp data.out $PBS_O_WORKDIR
